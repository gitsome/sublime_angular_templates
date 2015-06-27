import sublime, sublime_plugin, re

def getHtmlTemplateRegions(view):
    return view.find_all('template\s*\:\s*\[([\s\S]*)\]\.join\((\'\'|\"\")\)')

def convertStringToHtml(stringToConvert):
    lines = stringToConvert.splitlines()
    finalStringList = []
    for line in lines:
        firstCharMatches = re.match('^\s{0,}([^\s]{1})', line)
        if firstCharMatches:
            firstChar = firstCharMatches.group(1)
            if firstChar == '\'' or firstChar == '"':
                line = re.sub(r'^(\s{0,})([^\s]{1})', r'\1', line)
                line = re.sub(r'([\'\"]{1})(\s*)(?:\,)?(\s*)(\\\\.*|\s*)?$', r'\3\4', line)
                if firstChar == '\'':
                    line = re.sub(r"(\\')", r"'", line)
                if firstChar == '"':
                    line = re.sub(r'(\\")', r'"', line)

        finalStringList.append(line)

    return "\n".join(finalStringList)

def convertHtmlToString(htmlToConvert):
    lines = htmlToConvert.splitlines()
    finalStringList = []
    for line in lines:
        firstCharMatches = re.match('^\s*([^\s]{1})', line)
        lineCommented = re.match('^\s*\/\/', line)

        if firstCharMatches:
            firstChar = firstCharMatches.group(1)
            print lineCommented
            if firstChar != '\'' and firstChar != '"' and lineCommented == None:
                line = re.sub(r"(')", r"\'", line)
                line = re.sub(r'^(\s{0,})([^\s]{1})', r"\1'\2", line)
                line = re.sub(r'([^\s]{1})(\s*)(\\\\.*|\s*)?$', r"\1',\2\3", line)

        finalStringList.append(line)

    mergedString = "\n".join(finalStringList)
    mergedString = re.sub(r'(,)([\s\n]*)$', r"\2", mergedString)

    return mergedString


def htmlToString(self, view):
    htmlTemplateRegions = getHtmlTemplateRegions(view)
    for region in htmlTemplateRegions:
        edit = view.begin_edit()
        regionString = view.substr(region)
        for (templatePart, contentPart, joinStartPart, joinMiddlePart, joinEndPart) in re.findall('(template\s*\:\s*\[)([\s\S]*)(\]\.join\()(\'\'|\"\")(\))', regionString):
            newRegionString = templatePart + convertHtmlToString(contentPart) + joinStartPart + joinMiddlePart + joinEndPart
        print newRegionString
        view.replace(edit, region, newRegionString)
        view.end_edit(edit)

def stringToHtml(self, view):
    htmlTemplateRegions = getHtmlTemplateRegions(view)
    for region in htmlTemplateRegions:
        edit = view.begin_edit()
        regionString = view.substr(region)
        for (templatePart, contentPart, joinStartPart, joinMiddlePart, joinEndPart) in re.findall('(template\s*\:\s*\[)([\s\S]*)(\]\.join\()(\'\'|\"\")(\))', regionString):
            newRegionString = templatePart + convertStringToHtml(contentPart) + joinStartPart + joinMiddlePart + joinEndPart
        print newRegionString
        view.replace(edit, region, newRegionString)
        view.end_edit(edit)


def isAngularDirectiveFile(fileName):
    return re.match('.*\.dir\.js', fileName)


class AngularTemplates(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        if isAngularDirectiveFile(view.file_name()) != None:
            htmlToString(self, view)


class AngularTemplatesTransform(sublime_plugin.TextCommand):

    def run(self, edit):
        if isAngularDirectiveFile(self.view.file_name()) != None:
            stringToHtml(self, self.view)
