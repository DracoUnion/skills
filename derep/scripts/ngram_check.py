#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derep 确定性计算工具：文本分块 + n-gram 重复度检测。

用法：
  python ngram_check.py chunk --file <文件> [--limit 8000] [--out-dir <目录>]
  python ngram_check.py metrics --source <源文件> --copy <改写文件> [--n 3] [--threshold 0.4]

参数可以是文件路径（存在时读取）或文本本身。
"""
import argparse
import json
import os
import re
import sys

# 统一 UTF-8 输入输出，避免 Windows 控制台默认编码（如 GBK）导致乱码
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stdin, 'reconfigure'):
    try:
        sys.stdin.reconfigure(encoding='utf-8')
    except Exception:
        pass


def tok_en_zh(text):
    """分词：每个汉字单独成词，英文单词成词。"""
    return re.findall(r'[一-鿿]|[a-zA-Z]+', text)


def get_ngram_set(toks, n):
    return {tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)}


def ngram_jaccard(text1, text2, n):
    set1 = get_ngram_set(tok_en_zh(text1.lower()), n)
    set2 = get_ngram_set(tok_en_zh(text2.lower()), n)
    inter = len(set1 & set2)
    union = len(set1 | set2)
    return inter / union if union else 0.0


def ngram_coverage(src, gen, n):
    src_set = get_ngram_set(tok_en_zh(src.lower()), n)
    gen_set = get_ngram_set(tok_en_zh(gen.lower()), n)
    inter = len(src_set & gen_set)
    all_ = len(gen_set)
    return inter / all_ if all_ else 0.0


def split_md_lines(md):
    """按行拆分，代码块整体保留为一个分片。"""
    lines = md.split('\n')
    res = []
    in_code = False
    code = ''
    for l in lines:
        if '```' in l:
            if in_code:
                code += l
                res.append(code)
                code = ''
            else:
                code += l + '\n'
            in_code = not in_code
        elif not in_code:
            if l.strip():
                res.append(l)
        elif in_code:
            code += l + '\n'
    if code:
        res.append(code + '```')
    return res


def group_chunks(chunks, limit):
    groups = ['']
    for c in chunks:
        if len(groups[-1]) + len(c) + 2 > limit:
            groups.append(c)
        else:
            groups[-1] += '\n\n' + c
    return [g for g in groups if g]


def strip_placeholder(text):
    return re.sub(r'\[PRE\d+\]', '', text)


def check_code_blocks(source, copy):
    missing = [tk for tk in re.findall(r'\[PRE\d+\]', source) if tk not in copy]
    unknown = [tk for tk in re.findall(r'\[PRE\d+\]', copy) if tk not in source]
    return missing, unknown


def read_arg(arg):
    """参数既可以是文件路径（存在时读取），也可以是文本本身。"""
    if os.path.isfile(arg):
        with open(arg, encoding='utf-8') as f:
            return f.read()
    return arg


def cmd_chunk(args):
    md = read_arg(args.file) if args.file else sys.stdin.read()
    chunks = group_chunks(split_md_lines(md), args.limit)
    if args.out_dir:
        os.makedirs(args.out_dir, exist_ok=True)
        for i, c in enumerate(chunks):
            with open(os.path.join(args.out_dir, f'{i:03d}.md'), 'w', encoding='utf-8') as f:
                f.write(c)
    for i, c in enumerate(chunks):
        preview = c.split('\n')[0][:80]
        print(f'[{i:03d}] chars={len(c)} lines={c.count(chr(10)) + 1} head={preview!r}')
    print(f'total_chunks={len(chunks)}')


def cmd_metrics(args):
    source = read_arg(args.source)
    copy = read_arg(args.copy)
    s = strip_placeholder(source)
    c = strip_placeholder(copy)
    similarity = round(ngram_jaccard(s, c, args.n), 4)
    coverage = round(ngram_coverage(s, c, args.n), 4)
    src_set = get_ngram_set(tok_en_zh(s.lower()), args.n)
    gen_set = get_ngram_set(tok_en_zh(c.lower()), args.n)
    repeated = sorted(''.join(t) for t in (src_set & gen_set))
    is_duplicated = similarity >= args.threshold or coverage >= args.threshold
    missing, unknown = check_code_blocks(source, copy)
    result = {
        'n': args.n,
        'threshold': args.threshold,
        'ngram_similarity': similarity,
        'ngram_coverage': coverage,
        'is_duplicated': is_duplicated,
        'repeated_ngrams': repeated,
        'missing_blocks': missing,
        'unknown_blocks': unknown,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description='derep 确定性工具')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_chunk = sub.add_parser('chunk', help='按 limit 把文本分块（保留代码块整体）')
    p_chunk.add_argument('--file', help='输入文件（缺省读 stdin）')
    p_chunk.add_argument('--limit', type=int, default=8000)
    p_chunk.add_argument('--out-dir', help='若指定，把每块写入 <out>/000.md, 001.md ...')
    p_chunk.set_defaults(func=cmd_chunk)

    p_metrics = sub.add_parser('metrics', help='计算源文与改写文的 n-gram 重复度')
    p_metrics.add_argument('--source', required=True, help='源文（文件路径或文本）')
    p_metrics.add_argument('--copy', required=True, help='改写文（文件路径或文本）')
    p_metrics.add_argument('--n', type=int, default=3, help='n-gram 窗口大小')
    p_metrics.add_argument('--threshold', type=float, default=0.4, help='重复度阈值')
    p_metrics.set_defaults(func=cmd_metrics)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
