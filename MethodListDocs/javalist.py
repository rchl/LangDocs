import re
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

javaseurl = "https://docs.oracle.com/javase/8/docs/api/%s.html"
jfxurl = "https://docs.oracle.com/javase/8/javafx/api/%s.html"

def replaced(text):

    replace_text = text.replace("\\n", " ").replace("\\t", "").replace("\\r", "").replace("&nbsp;", " ").replace("\'", "'").replace("&quot;", "\"").replace("\\;", "").replace("\\'", "'").replace("&lt;", "<").replace("&gt;", ">").replace("&#8220;", "\"").replace("&#8221;", "\"").replace("\xe2\x80\x94", " -- ").replace("\\xe2\\x80\\x94", " -- ").replace("&#8217;", "'").replace("&para;", "|").replace("&uarr", "↑").replace("\xe2\x80\x98", "'").replace("\\xe2\\x80\\x98", "'").replace("\xe2\x80\x99", "'").replace("\\xe2\\x80\\x99", "'").replace("\xe2\x80\x9c", "\"").replace("\\xe2\\x80\\x9c", "\"").replace("\xe2\x80\x9c", "\"").replace("\\xe2\\x80\\x9c", "\"").replace("\xe2\x80\x9d", "\"").replace("\\xe2\\x80\\x9d", "\"").replace("\xe2\x80\x9d", "\"").replace("\\xe2\\x80\\x9d", "\"").replace("\xe2\x80\x93", "-").replace("\\xe2\\x80\\x93", "-").replace("\\xc2\\xa0", " ").replace("\xc2\xa0", " ").replace("&#8217;", "'").replace("&#8212;", "--").replace("&ndash;", "--")

    return replace_text

def getMethods(text):
    text = text.replace(".", "/")

    try:
        link = javaseurl % text
        classurl = replaced(str(urlopen(link).read()))

        class_data = re.findall(r'<meta name="keywords" content="(.*?)">', classurl)[1:]

    except:
        link = jfxurl % text
        classurl = replaced(str(urlopen(link).read()))

        class_data = re.findall(r'<td class="colLast"><code><span class=".*?--">(.*?)</code>', classurl)

    fields = "Fields are:\n"; fields += "%s\n" % ("=" * (len(fields) - 1))
    methods = "\nMethods are:\n"; methods += "%s\n" % ("=" * (len(methods) - 1))

    pattern = re.compile(r'<.*?>|\\n')

    result = []
    for x in class_data:
        if "." not in x:
            x = x.split(" ")[0]
            result.append("%s" % (pattern.sub("", x)))

    for x in sorted(set(result)):
        if x.endswith("()"):
           methods += "%s, " % x
        else:
            fields += "%s, " % x
    methods += "\n"
    fields += "\n"

    return (fields + methods, link)