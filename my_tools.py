import os
import json
import hashlib
import datetime
from typing import Any, Dict, List, Optional, Union
import re
class MyTools:
    @staticmethod
    def file_info(filepath: str) -> Dict[str, Any]:
        try:
            if not os.path.exists(filepath):
                return {'error': f'文件不存在: {filepath}'}
            stat = os.stat(filepath)
            return {'filepath': filepath, 'exists': True, 'size': stat.st_size, 'created': datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(), 'modified': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(), 'is_file': os.path.isfile(filepath), 'is_dir': os.path.isdir(filepath), 'extension': os.path.splitext(filepath)[1], 'filename': os.path.basename(filepath), 'directory': os.path.dirname(filepath)}
        except Exception as e:
            return {'error': str(e)}
    @staticmethod
    def calculate_md5(filepath: str) -> str:
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            return f'Error: {str(e)}'
    @staticmethod
    def count_words(text: str) -> Dict[str, int]:
        lines = text.split('\n')
        words = re.findall('\\b\\w+\\b', text)
        return {'characters': len(text), 'characters_no_spaces': len(text.replace(' ', '').replace('\n', '').replace('\t', '')), 'words': len(words), 'lines': len(lines), 'non_empty_lines': len([line for line in lines if line.strip()]), 'average_word_length': sum((len(word) for word in words)) / len(words) if words else 0}
    @staticmethod
    def search_in_file(filepath: str, search_term: str, case_sensitive: bool=False) -> List[Dict[str, Any]]:
        try:
            if not os.path.exists(filepath):
                return [{'error': f'文件不存在: {filepath}'}]
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            pattern = search_term if case_sensitive else search_term.lower()
            text_to_search = content if case_sensitive else content.lower()
            results = []
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                line_to_search = line if case_sensitive else line.lower()
                if pattern in line_to_search:
                    start_pos = line_to_search.find(pattern)
                    results.append({'line_number': i, 'line_content': line, 'match_position': start_pos, 'match_length': len(pattern), 'context': line[max(0, start_pos - 20):start_pos + len(pattern) + 20]})
            return results
        except Exception as e:
            return [{'error': str(e)}]
    @staticmethod
    def format_json(data: Union[str, Dict, List], indent: int=2) -> str:
        try:
            if isinstance(data, str):
                parsed = json.loads(data)
            else:
                parsed = data
            return json.dumps(parsed, indent=indent, ensure_ascii=False)
        except Exception as e:
            return f'Error formatting JSON: {str(e)}'
    @staticmethod
    def list_files(directory: str='.', pattern: str='*') -> List[Dict[str, Any]]:
        try:
            if not os.path.exists(directory):
                return [{'error': f'目录不存在: {directory}'}]
            files = []
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                stat = os.stat(item_path)
                if pattern != '*':
                    if not re.match(pattern.replace('*', '.*').replace('?', '.'), item):
                        continue
                files.append({'name': item, 'path': item_path, 'is_file': os.path.isfile(item_path), 'is_dir': os.path.isdir(item_path), 'size': stat.st_size if os.path.isfile(item_path) else 0, 'modified': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()})
            return sorted(files, key=lambda x: x['name'])
        except Exception as e:
            return [{'error': str(e)}]
    @staticmethod
    def create_backup(filepath: str, backup_dir: str='backups') -> Dict[str, Any]:
        try:
            if not os.path.exists(filepath):
                return {'error': f'文件不存在: {filepath}'}
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.basename(filepath)
            backup_name = f'{filename}.backup_{timestamp}'
            backup_path = os.path.join(backup_dir, backup_name)
            import shutil
            shutil.copy2(filepath, backup_path)
            return {'original': filepath, 'backup': backup_path, 'timestamp': timestamp, 'size': os.path.getsize(backup_path), 'md5': MyTools.calculate_md5(backup_path)}
        except Exception as e:
            return {'error': str(e)}
tools = MyTools()
def test_tools():
    print('=== 测试自定义工具 ===')
    print('\n1. 测试文件信息:')
    info = tools.file_info(__file__)
    print(json.dumps(info, indent=2, ensure_ascii=False))
    print('\n2. 测试MD5计算:')
    md5 = tools.calculate_md5(__file__)
    print(f'MD5: {md5}')
    print('\n3. 测试字数统计:')
    sample_text = 'Hello World!\nThis is a test.\nAnother line here.'
    stats = tools.count_words(sample_text)
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    print('\n4. 测试文件搜索:')
    search_results = tools.search_in_file(__file__, 'def', case_sensitive=False)
    print(f'找到 {len(search_results)} 个匹配项')
    for i, result in enumerate(search_results[:3], 1):
        print(f"  匹配 {i}: 第{result['line_number']}行")
    print('\n5. 测试JSON格式化:')
    test_data = {'name': '测试', 'value': 123, 'list': [1, 2, 3]}
    formatted = tools.format_json(test_data)
    print(formatted)
    print('\n6. 测试文件列表:')
    files = tools.list_files('.', '*.py')
    print(f'找到 {len(files)} 个.py文件')
    for file in files[:3]:
        print(f"  - {file['name']} ({file['size']} bytes)")
    print('\n=== 测试完成 ===')
if __name__ == '__main__':
    test_tools()