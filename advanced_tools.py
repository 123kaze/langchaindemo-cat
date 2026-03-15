import os
import json
import re
import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter
import hashlib
class AdvancedTools:
    @staticmethod
    def analyze_text_file(filepath: str) -> Dict[str, Any]:
        try:
            if not os.path.exists(filepath):
                return {'error': f'文件不存在: {filepath}'}
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            lines = content.split('\n')
            words = re.findall('\\b\\w+\\b', content)
            sentences = re.split('[.!?。！？]+', content)
            word_freq = Counter(words)
            top_words = word_freq.most_common(10)
            line_lengths = [len(line) for line in lines]
            avg_line_length = sum(line_lengths) / len(line_lengths) if line_lengths else 0
            char_counter = Counter(content)
            total_chars = len(content)
            with open(filepath, 'rb') as f:
                raw_content = f.read()
            encoding = 'utf-8'
            try:
                raw_content.decode('utf-8')
            except:
                encoding = 'unknown'
            line_endings = 'LF'
            if b'\r\n' in raw_content:
                line_endings = 'CRLF'
            elif b'\r' in raw_content:
                line_endings = 'CR'
            return {'file_info': {'path': filepath, 'size': len(raw_content), 'encoding': encoding, 'line_endings': line_endings, 'md5': hashlib.md5(raw_content).hexdigest()}, 'statistics': {'total_chars': total_chars, 'total_lines': len(lines), 'total_words': len(words), 'total_sentences': len([s for s in sentences if s.strip()]), 'non_empty_lines': len([line for line in lines if line.strip()]), 'avg_line_length': round(avg_line_length, 2), 'max_line_length': max(line_lengths) if line_lengths else 0, 'min_line_length': min(line_lengths) if line_lengths else 0}, 'word_analysis': {'unique_words': len(word_freq), 'top_words': [{'word': w, 'count': c} for w, c in top_words], 'avg_word_length': sum((len(w) for w in words)) / len(words) if words else 0}, 'character_analysis': {'letters': sum((1 for c in content if c.isalpha())), 'digits': sum((1 for c in content if c.isdigit())), 'spaces': sum((1 for c in content if c.isspace())), 'punctuation': sum((1 for c in content if c in '.,!?;:"\'()[]{}')), 'other_chars': total_chars - sum((1 for c in content if c.isalnum() or c.isspace() or c in '.,!?;:"\'()[]{}'))}}
        except Exception as e:
            return {'error': str(e)}
    @staticmethod
    def compare_files(file1: str, file2: str) -> Dict[str, Any]:
        try:
            if not os.path.exists(file1):
                return {'error': f'文件1不存在: {file1}'}
            if not os.path.exists(file2):
                return {'error': f'文件2不存在: {file2}'}
            with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
                content1 = f1.read()
                content2 = f2.read()
            md5_1 = hashlib.md5(content1).hexdigest()
            md5_2 = hashlib.md5(content2).hexdigest()
            try:
                text1 = content1.decode('utf-8')
                text2 = content2.decode('utf-8')
                lines1 = text1.split('\n')
                lines2 = text2.split('\n')
                diff_lines = []
                for i, (line1, line2) in enumerate(zip(lines1, lines2), 1):
                    if line1 != line2:
                        diff_lines.append({'line': i, 'file1': line1[:100] + ('...' if len(line1) > 100 else ''), 'file2': line2[:100] + ('...' if len(line2) > 100 else '')})
                if len(lines1) != len(lines2):
                    for i in range(min(len(lines1), len(lines2)), max(len(lines1), len(lines2))):
                        diff_lines.append({'line': i + 1, 'file1': lines1[i] if i < len(lines1) else '(文件结束)', 'file2': lines2[i] if i < len(lines2) else '(文件结束)'})
                is_text = True
            except:
                is_text = False
                diff_lines = []
            return {'files': {'file1': {'path': file1, 'size': len(content1), 'md5': md5_1}, 'file2': {'path': file2, 'size': len(content2), 'md5': md5_2}}, 'comparison': {'identical': md5_1 == md5_2, 'size_equal': len(content1) == len(content2), 'is_text_file': is_text, 'size_difference': abs(len(content1) - len(content2)), 'size_ratio': len(content1) / len(content2) if len(content2) > 0 else float('inf')}, 'differences': {'total_differences': len(diff_lines), 'diff_lines': diff_lines[:20]} if is_text else {'message': '二进制文件，无法进行文本比较'}}
        except Exception as e:
            return {'error': str(e)}
    @staticmethod
    def extract_code_blocks(text: str, language: str='python') -> List[Dict[str, Any]]:
        patterns = {'python': ['```python\\s*(.*?)\\s*```', '```\\s*(.*?)\\s*```', 'def\\s+\\w+\\s*\\(.*?\\):.*?(?=\\n\\s*\\n|\\Z)', 'class\\s+\\w+.*?:.*?(?=\\n\\s*\\n|\\Z)'], 'javascript': ['```javascript\\s*(.*?)\\s*```', '```js\\s*(.*?)\\s*```', 'function\\s+\\w+\\s*\\(.*?\\)\\s*{.*?}'], 'html': ['```html\\s*(.*?)\\s*```', '<[^>]+>.*?</[^>]+>']}
        code_blocks = []
        patterns_to_use = patterns.get(language, patterns['python'])
        for pattern in patterns_to_use:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match else ''
                code_blocks.append({'code': match.strip(), 'pattern': pattern[:50] + '...' if len(pattern) > 50 else pattern, 'language': language})
        unique_blocks = []
        seen = set()
        for block in code_blocks:
            code_hash = hashlib.md5(block['code'].encode()).hexdigest()
            if code_hash not in seen:
                seen.add(code_hash)
                unique_blocks.append(block)
        return unique_blocks
    @staticmethod
    def batch_process_files(directory: str, pattern: str='*.txt', processor: str='analyze') -> List[Dict[str, Any]]:
        try:
            if not os.path.exists(directory):
                return [{'error': f'目录不存在: {directory}'}]
            import fnmatch
            results = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if fnmatch.fnmatch(file, pattern):
                        filepath = os.path.join(root, file)
                        if processor == 'analyze':
                            result = AdvancedTools.analyze_text_file(filepath)
                            result['filepath'] = filepath
                            results.append(result)
                        elif processor == 'count':
                            with open(filepath, 'r', encoding='utf-8') as f:
                                content = f.read()
                            words = re.findall('\\b\\w+\\b', content)
                            results.append({'filepath': filepath, 'word_count': len(words), 'line_count': len(content.split('\n')), 'size': os.path.getsize(filepath)})
                        elif processor == 'search':
                            results.append({'filepath': filepath, 'message': '搜索功能待实现'})
            return results
        except Exception as e:
            return [{'error': str(e)}]
    @staticmethod
    def create_project_report(project_dir: str='.') -> Dict[str, Any]:
        try:
            if not os.path.exists(project_dir):
                return {'error': f'项目目录不存在: {project_dir}'}
            report = {'project_info': {'directory': os.path.abspath(project_dir), 'scan_time': datetime.datetime.now().isoformat(), 'total_size': 0}, 'file_types': {}, 'code_stats': {'total_files': 0, 'total_lines': 0, 'total_words': 0, 'by_language': {}}, 'recent_files': []}
            file_extensions = {}
            total_size = 0
            for root, dirs, files in os.walk(project_dir):
                if '.git' in root or '__pycache__' in root or '.idea' in root:
                    continue
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        size = os.path.getsize(filepath)
                        total_size += size
                        ext = os.path.splitext(file)[1].lower()
                        if ext:
                            file_extensions[ext] = file_extensions.get(ext, 0) + 1
                        if ext in ['.py', '.js', '.java', '.cpp', '.c', '.h', '.html', '.css']:
                            try:
                                with open(filepath, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                lines = len(content.split('\n'))
                                words = len(re.findall('\\b\\w+\\b', content))
                                lang = ext[1:]
                                if lang not in report['code_stats']['by_language']:
                                    report['code_stats']['by_language'][lang] = {'files': 0, 'lines': 0, 'words': 0}
                                report['code_stats']['by_language'][lang]['files'] += 1
                                report['code_stats']['by_language'][lang]['lines'] += lines
                                report['code_stats']['by_language'][lang]['words'] += words
                                report['code_stats']['total_files'] += 1
                                report['code_stats']['total_lines'] += lines
                                report['code_stats']['total_words'] += words
                            except:
                                pass
                        mtime = os.path.getmtime(filepath)
                        report['recent_files'].append({'file': file, 'path': os.path.relpath(filepath, project_dir), 'size': size, 'modified': datetime.datetime.fromtimestamp(mtime).isoformat()})
                    except:
                        continue
            report['project_info']['total_size'] = total_size
            report['file_types'] = dict(sorted(file_extensions.items(), key=lambda x: x[1], reverse=True))
            report['recent_files'].sort(key=lambda x: x['modified'], reverse=True)
            report['recent_files'] = report['recent_files'][:10]
            return report
        except Exception as e:
            return {'error': str(e)}
advanced_tools = AdvancedTools()
def test_advanced_tools():
    print('=== 测试高级工具 ===')
    print('\n1. 测试文本文件分析:')
    analysis = advanced_tools.analyze_text_file('my_tools.py')
    if 'error' not in analysis:
        print(f"文件: {analysis['file_info']['path']}")
        print(f"大小: {analysis['file_info']['size']} 字节")
        print(f"行数: {analysis['statistics']['total_lines']}")
        print(f"单词数: {analysis['statistics']['total_words']}")
        print(f"最常用单词: {analysis['word_analysis']['top_words'][0]}")
    else:
        print(f"错误: {analysis['error']}")
    print('\n2. 测试文件比较:')
    comparison = advanced_tools.compare_files('my_tools.py', 'test_my_tools.py')
    if 'error' not in comparison:
        print(f"文件相同: {comparison['comparison']['identical']}")
        print(f"大小相等: {comparison['comparison']['size_equal']}")
        print(f"差异行数: {comparison['differences']['total_differences']}")
    else:
        print(f"错误: {comparison['error']}")
    print('\n3. 测试代码块提取:')
    with open('my_tools.py', 'r', encoding='utf-8') as f:
        python_code = f.read()
    code_blocks = advanced_tools.extract_code_blocks(python_code, 'python')
    print(f'提取到 {len(code_blocks)} 个代码块')
    for i, block in enumerate(code_blocks[:3], 1):
        print(f"  代码块 {i}: {len(block['code'])} 字符")
    print('\n4. 测试项目报告:')
    report = advanced_tools.create_project_report('.')
    if 'error' not in report:
        print(f"项目目录: {report['project_info']['directory']}")
        print(f"总大小: {report['project_info']['total_size']} 字节")
        print(f"文件类型统计: {list(report['file_types'].items())[:5]}")
        print(f"代码文件数: {report['code_stats']['total_files']}")
    else:
        print(f"错误: {report['error']}")
    print('\n=== 测试完成 ===')
if __name__ == '__main__':
    test_advanced_tools()