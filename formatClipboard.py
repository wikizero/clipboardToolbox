"""
@Author  :   Name: Vance  Email: 937316808@qq.com
@Time    :   2019/07/03
@Desc    :   格式化粘贴板的数据
    1、转成list、dict、dataFrame、json等格式，转指定格式后可以直接赋值给变量
    2、支持导出文件，支持文件格式包括普通文本、csv、excel等
    3、支持生成Python代码，list、dict、dataFrame、json等Python代码生成
"""
import re
import time
import json
import threading
from collections import deque

import pandas as pd
import pyperclip
from pylsy import pylsytable


class ExtendString(str):
    """
    扩展python内置str类，添加to方法等
    """
    def __init__(self, obj):
        self.obj = obj
        super(ExtendString, self).__init__()

    def to(self, fm, **kwargs):
        return self.format_(fm, **kwargs)

    def format_(self, fm, in_sep: str = '\s+', out_sep: str = None, **param):
        """
        :param fm: 'list', 'df', 'dict'

        指定df可选参数: encoding 编码
                      index_col 第几行做索引
                      names 字段名

        指定list可选参数: sep 分隔符(支持正则)
                        maxsplit,flag 用法参考re.split

        :param in_sep: separator for input string
        :param out_sep: separator for output string

        :return: 格式化后数据
        """
        if fm == 'df':
            param.setdefault('header', None)
            return pd.read_clipboard(**param)
        elif fm == 'list':
            lst = re.split(pattern=in_sep, string=self.obj, **param)
            lst = [i.strip() for i in lst if i.strip()]
            return lst if out_sep is None else out_sep.join(lst)

    def out(self, content, filename):
        """
        dict: json, plain text, excel
        df: excel, csv, plain text
        list: plain text
        """
        if filename.endswith('.xlsx'):
            with pd.ExcelWriter(filename) as writer:
                content.to_excel(writer, index=None)
                writer.save()
        elif filename.endswith('.csv'):
            pass
        elif filename.endswith('.json'):
            json.dump(content, open(filename, 'w+'))
        else:
            with open(filename, 'w+') as fp:
                fp.write('\n'.join(content))

    def format_web(self):
        '''
            将网页复制过来的cookies、headers转化成字典
        :return: dict
        '''
        ret = self.format_('list', sep='\n')
        return dict([i.split(':', 1) for i in ret])


class FormatClipboard():

    def __init__(self):
        self.max_len = 5
        self.stack = deque(maxlen=self.max_len)

    def get_text(self):
        """
        get text from clipboard
        :return:
        """
        text = pyperclip.paste().strip()
        # if not text:
        #     raise Exception('Nothing in your clipboard')
        return text

    def show_history(self):
        if len(self.stack) == 0:
            print()

        first, *lst = [re.sub('\s+', ' ', row[:27]+'...' if len(row) > 30 else row) for row in self.stack.copy()][::-1]
        table = pylsytable(['$0', first])
        table.append_data('$0', [f'${i + 1}' for i in range(len(lst))])
        table.append_data(first, lst)
        print(table, end='')

    def clipboard_watcher(self):
        recent_value = ''
        while True:
            tmp_value = self.get_text()
            if tmp_value != '' and tmp_value != recent_value:
                recent_value = tmp_value
                self.stack.append(recent_value)
                # print('Value changed:')
                # self.show_history()
            time.sleep(0.5)

    def command(self):
        lst = [f'${i + 1}' for i in range(self.max_len)]
        while True:
            text = input('>>>').strip()

            if text in ('', 'show', 'ls'):
                self.show_history()
                continue

            # 拓展系统str类 增加to方法
            text = re.sub('\$(\d+)', r'ExtendString($[\1])', text)

            text = text.replace('$', 'list(self.stack.copy())[::-1]')

            code = f'print({text})'

            try:
                exec(code)
            except Exception as e:
                pass
            # elif text in lst:
            #     print(list(self.stack.copy())[::-1][lst.index(text)])

    def main(self):
        t = threading.Thread(target=self.clipboard_watcher, name='clipboard_watcher')
        t.setDaemon(True)
        t.start()

        self.command()


if __name__ == '__main__':
    # TODO 读取内存的文件
    # TODO 输出参考代码
    # TODO markdown 转换 (自动识别)
    # TODO 分组  N 个一组
    # TODO 命令行工具  操作
    # TODO 如何实现链式调用的？

    # TODO 先整理需求场景 !!!
    # pickup headq
    # text = FormatClipboard().format_('list', in_sep='\n', out_sep='\t')
    # text = FormatClipboard().format_('df')
    # print(text)
    FormatClipboard().main()
