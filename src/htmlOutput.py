#coding:utf8
"""
Created on 2016年1月11日

@author: pan
"""


class HtmlOutput(object):
    def __init__(self):
        self.datas =[]
        self.index_datas = list()
        self.fisrt_user_data = list()

        
    
    def collect_data(self, data):
        if data is None:
            return None
        self.datas.append(data)

    def collect_index_data(self, datas):
        if datas is None:
            return None
        self.index_datas.append(datas)

    def collect_user_data(self, datas):
        if datas is None:
            return None
        self.fisrt_user_data.append(datas)

    def get_index_data(self):
        return self.index_datas

    def clear_index_data(self):
        self.index_datas=list()


    
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
    

    def output_user_html(self, file_path):
        fout = open(file_path, 'w')
        fout.write("<html>")
        fout.write("<head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /></head>")
        fout.write("<body>")
        fout.write("<table border=\"1\" cellpadding=\"0\" cellspacing=\"0\">")
        fout.write("<tr><th>昵称</th><th>介绍</th><th>地址</th><th>方向</th><th>性别</th><th>公司</th><th>职业</th>"
                   "<th>学校</th><th>专业</th><th>主页</th><</tr>")

        for data in self.fisrt_user_data:
                fout.write("<tr>")
                fout.write("<td>%s</td>" % data['name'].encode('utf-8'))
                fout.write("<td>%s</td>" % data['bio'].encode('utf-8'))
                fout.write("<td>%s</td>" % data['location'].encode('utf-8'))
                fout.write("<td>%s</td>" % data['business'].encode('utf-8'))
                fout.write("<td>%s</td>" % data['gender'].encode('utf-8'))
                fout.write("<td>%s</td>" % data['employment'].encode('utf-8'))
                fout.write("<td>%s</td>" % data['position'].encode('utf-8'))
                fout.write("<td>%s</td>" % data['school'].encode('utf-8'))
                fout.write("<td>%s</td>" % data['major'].encode('utf-8'))
                fout.write("<td><a href=\"%s\">%s</a></td>" %(data['url'].encode('utf-8'), data['url'].encode('utf-8')))
                fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()
    
    



