class FormatContent():
    def format_content(self,content):
        html_1 = "<html><head><style type='text/css'>div{" \
            "width : 100%;" \
            "}" \
            "p{" \
            "    text-indent: 2em;" \
            "    font-family: 'Merriweather Sans',Open Sans,Helvetica,Arial,sans-serif;" \
            "    font-size: 1rem;" \
            "    font-weight: lighter;" \
            "    line-height: 120%;" \
            "    margin: 0 0 10px;" \
            "    padding: 15px 15px 15px 15px;" \
            "    color: black;"\
            "}" \
            "img" \
            "{" \
            " display:block; " \
            " margin:0 auto;" \
            "width: 100%;" \
            "display: block;" \
            "margin: auto;" \
            "}" \
            "a{" \
            " color: #2ba4eb;" \
            " text-decoration: none;" \
            "}" \
            "</style>" \
            "</head>" \
            "<body>" \
            "<div>"
        html_2='''</div></body></html>'''
        text = content.replace("\n","").replace("\r","").replace("\t","")
        return html_1 +text +html_2

