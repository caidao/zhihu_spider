#coding:utf8
"""
Created on 2016年1月11日

@author: pan
"""


class HtmlOutput(object):
    def __init__(self):
        self.datas =[]
        self.index_datas = list()
        
    
    def collect_data(self, data):
        if data is None:
            return None
        self.datas.append(data)

    def collect_index_data(self, datas):
        if datas is None:
            return None
        self.index_datas.append(datas)



    
    def output_html(self, file_path):
        fout = open(file_path, 'w')
        fout.write("<html>")
        fout.write("<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head>")
        fout.write("<body>")
        fout.write("<table>")
        
        for datalist in self.index_datas:
            for data in datalist:
                fout.write("<tr>")
                fout.write("<td><a href=\"%s\">%s</a></td>" % (data['url'].encode('utf-8'), data['url'].encode('utf-8')))
                fout.write("<td>%s</td>" % data['title'].encode('utf-8'))
                fout.write("<td>%s</td>" % data['source'].encode('utf-8'))
                fout.write("</tr>")
        
        fout.write("</table>")
        fout.write("</body>") 
        fout.write("</html>")
        fout.close()
        pass
    
    
    
    



