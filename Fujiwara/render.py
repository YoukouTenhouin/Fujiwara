import misaka as m
import hashlib
from misaka import Markdown, HtmlRenderer, SmartyPants
from pygments import highlight
from pygments.lexers import get_lexer_by_name,guess_lexer
from pygments.formatters import HtmlFormatter

# Create a custom renderer


class BleepRenderer(HtmlRenderer, SmartyPants):
    def preprocess(self, text):
        return text.replace('\n','\n\n')

    def block_code(self, text, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % text.replace('\n\n','\n').strip()
        elif lang == "math":
            return "\n%s\n" % text.replace('\n\n','\n')
            
        try:
            lexer = get_lexer_by_name(lang.lower(), stripall=True)
        except:
            lexer = guess_lexer(text)
            
        formatter = HtmlFormatter()
        return highlight(text.replace('\n\n','\n'), lexer, formatter)

# And use the renderer
renderer = BleepRenderer(flags = m.HTML_ESCAPE)
md = Markdown(renderer,
                extensions=m.EXT_FENCED_CODE | m.EXT_STRIKETHROUGH)

def render(markdown):
    return md.render(markdown)
