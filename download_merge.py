import os
import requests
import lxml.html
from PyPDF2 import PdfFileMerger

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'}

# 网页URL
web_pages = ['http://speech.ee.ntu.edu.tw/~tlkagk/courses_MLDS18.html',
             'http://speech.ee.ntu.edu.tw/~tlkagk/courses_ML17_2.html']

# 创建一个目录 用于保存合并前的所有PDF
def CreateDir(url):
    folder_path = url.split("/")[-1].split('.')[0]
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return folder_path

# 下载单个PDF
def savePDF(fp, pdf_url, pdf_name):
    try:
        res = requests.get(pdf_url, headers=headers, stream=True).content
        with open(os.path.join(fp, pdf_name), "wb") as pdf_file:
            pdf_file.write(res)
    except:
        print('Exception occur in downloading a PDF')

    print(pdf_name + ' down finished!')

# 下载URL所有PDF文件
def Down(fp, url):
    try:
        res = requests.request("get", url=url, timeout=10000).text # text->unicode content->bytes for file or pic
        tree = lxml.html.fromstring(res)
        for node in tree.xpath('//a[re:test(@href, "\.pdf$", "i")]', namespaces={'re': 'http://exslt.org/regular-expressions'}):
            savePDF(fp, url[0 : url.rfind('/', 1)+1] + node.attrib['href'], node.attrib['href'].split("/")[-1])
    except:
        print('Exception occur in finding PDF links')

    print(url + ' down finished!')
    print('#############################################################')

# 将该文件路径下所有PDF文件按时间顺序合并 输出到根目录下
def Merge(fp):
    merger = PdfFileMerger()
    items = [(fp + '/' + i, os.stat(fp + '/' + i).st_mtime) for i in os.listdir(fp)] # use downloading timeline
    for item in sorted(items, key=lambda x: x[1]):
        try:
            merger.append(item[0]) # append a pdf
        except:
            print('Exception occur in merging ' + item[0])
            continue

    try:
        folder_name = fp.split('/')[-1]
        with open(folder_name + '_Merge.pdf', "wb") as pdf_file:
            merger.write(pdf_file)
    except:
        os.remove(folder_name + '_Merge.pdf')
        print('Exception occur in writing merged PDF -> Delete')
        print('#############################################################')

    print(url + ' merge finished!')
    print('#############################################################')

if __name__ == "__main__":
    for url in web_pages:
        fp = CreateDir(url)
        Down(fp, url)
        Merge(fp)
