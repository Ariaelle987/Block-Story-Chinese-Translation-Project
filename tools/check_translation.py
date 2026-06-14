import os
import re
import sys
from collections import defaultdict

# ========== 配置区 ==========
# 跳过检测的 msgid（不检查漏翻和占位符）
SKIP_MSGID = {
    "Note Empty",
    "Failed to upload world {0}, {1}",
}

# 跳过检测的文件名（整个文件跳过）
SKIP_FILES = {
    # "Example.txt",
}
# ===========================

def normalize_placeholder(text):
    """规范化占位符：移除空格，统一格式"""
    if not text:
        return text
    text = re.sub(r'\s+', '', text)
    return text

def extract_placeholders(text):
    """提取所有占位符，返回规范化后的集合"""
    raw = set(re.findall(r'\{([^}]+)\}', text))
    return {normalize_placeholder(p) for p in raw}

def parse_po(filepath):
    """解析 PO 文件，返回 [(msgid, msgstr, line_number), ...]"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    entries = []
    msgid = None
    msgstr = None
    msgid_line = 0
    in_msgid = False
    in_msgstr = False
    buffer = []
    
    for line_num, line in enumerate(lines, start=1):
        line = line.rstrip('\n')
        
        # 跳过纯注释行
        if line.startswith('#') and not line.startswith('#,'):
            continue
        
        # msgid 开始
        if line.startswith('msgid'):
            if msgid is not None:
                entries.append((msgid, msgstr if msgstr is not None else '', msgid_line))
            
            if line == 'msgid ""':
                msgid = ''
                msgid_line = line_num
                in_msgid = True
                in_msgstr = False
                buffer = []
            else:
                match = re.match(r'msgid\s+"(.*)"', line)
                msgid = match.group(1) if match else ''
                msgid_line = line_num
                in_msgid = False
                in_msgstr = False
                buffer = []
            msgstr = None
        
        # msgstr 开始
        elif line.startswith('msgstr'):
            if line == 'msgstr ""':
                msgstr = ''
                in_msgstr = True
                in_msgid = False
                buffer = []
            else:
                match = re.match(r'msgstr\s+"(.*)"', line)
                msgstr = match.group(1) if match else ''
                in_msgstr = False
                in_msgid = False
                buffer = []
        
        # 多行续行
        elif line.startswith('"') and (in_msgid or in_msgstr):
            content = line.strip().strip('"')
            buffer.append(content)
            if in_msgid:
                msgid = ''.join(buffer)
            elif in_msgstr:
                msgstr = ''.join(buffer)
    
    if msgid is not None:
        entries.append((msgid, msgstr if msgstr is not None else '', msgid_line))
    
    # 过滤掉 header 条目
    return [(mid, mstr, line) for mid, mstr, line in entries if mid and mid != '']

def check_translation(msgid, msgstr, path, line_num):
    """检查单条翻译，返回错误列表"""
    errors = []
    
    # 白名单跳过
    if msgid in SKIP_MSGID:
        return errors
    
    # 1. 漏翻检查
    if not msgstr or msgstr.strip() == '':
        errors.append(f"{path}:{line_num} 未翻译 -> {msgid[:80]}")
        return errors
    
    # 2. 占位符缺失检查
    id_placeholders = extract_placeholders(msgid)
    str_placeholders = extract_placeholders(msgstr)
    
    missing = id_placeholders - str_placeholders
    if missing:
        raw_missing = [p for p in re.findall(r'\{([^}]+)\}', msgid) 
                       if normalize_placeholder(p) in missing]
        errors.append(f"{path}:{line_num} 缺失占位符 {raw_missing} -> {msgid[:60]}")
    
    return errors

def main():
    errors = []
    po_files = []
    
    # 收集所有 .txt 文件
    for root, _, files in os.walk('.'):
        for f in files:
            if f.endswith('.txt'):
                po_files.append(os.path.join(root, f))
    
    # 过滤跳过的文件
    po_files = [f for f in po_files if os.path.basename(f) not in SKIP_FILES]
    
    print(f"找到 {len(po_files)} 个 PO 文件")
    
    # 记录每个文件内的 msgid
    file_msgid_map = defaultdict(lambda: defaultdict(list))
    
    for path in po_files:
        try:
            entries = parse_po(path)
            for msgid, msgstr, line_num in entries:
                file_msgid_map[path][msgid].append((msgstr, line_num))
                
                errs = check_translation(msgid, msgstr, path, line_num)
                errors.extend(errs)
        except Exception as e:
            errors.append(f"{path} 解析异常 - {e}")
    
    # 同一文件内重复翻译不一致检测
    for filepath, msgids in file_msgid_map.items():
        for msgid, translations in msgids.items():
            if len(translations) > 1:
                # 按翻译内容分组
                trans_map = defaultdict(list)
                for msgstr, line_num in translations:
                    trans_map[msgstr].append(line_num)
                
                if len(trans_map) > 1:
                    errors.append(f"\n{filepath} 同一 msgid 翻译不一致:")
                    errors.append(f"  msgid: {msgid[:70]}")
                    for trans, lines in trans_map.items():
                        preview = trans[:50] + "..." if len(trans) > 50 else trans
                        lines_str = ','.join(str(l) for l in lines)
                        errors.append(f"    行 {lines_str}: {preview}")
    
    # 输出结果
    if errors:
        print("\n翻译检查失败\n")
        for e in errors:
            print(e)
        sys.exit(1)
    else:
        print("\n翻译检查通过")
        print(f"  - 检查了 {len(po_files)} 个文件")
        print("  - 无未翻译条目")
        print("  - 无缺失占位符")
        print("  - 无重复翻译不一致")

if __name__ == "__main__":
    main()
