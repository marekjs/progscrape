import re
import unittest

__all__ = [ 'extractTags', 'displayTags', 'replaceInternal', 'isSymbol' ]

RAW_TAGS = [
    # General types of story
    { 'tag': 'video(s)', 'host': { 'youtube.com', 'vimeo.com' } },
    'music', 
    'audio', 
    'tutorial(s)', 
    'media', 
    'rfc',
    { 'tag': 'release', 'alt': { 'released', 'releases' } },
    'game(s)',

    # General concepts
    'algorithm(s)', 
    'compiler(s)', 
    { 'tag': '3d', 'alt': ['3 d', 'three dimension(s)', 'three dimensional'] }, 
    'hash', 
    'web', 
    'api',
    'spam',

    # Concrete concepts
    'drm', 
    'nosql', 
    'sql', 
    'copyright(s)', 
    'trademark(s)', 
    'patent(s)', 
    'encryption', 
    'economy', 
    'investing',
    'privacy', 
    'autism', 
    'lawsuit', 
    'universe', 
    'assembler(s)', 
    'proxy', 
    'censorship', 
    'firewall', 
    'trial',
    'piracy', 
    'ipo(s)', 
    'graphics', 
    'embedded', 
    'art', 
    'kernel', 
    'antimatter', 
    'compression',
    'font(s)',
    'concurrency',
    'beer',
    { 'tag': 'debugging', 'alt': [ 'debugger', 'debug', 'debugs' ]},

    # Orgs
    'amd', 
    'intel', 
    'apple', 
    'facebook', 
    'google', 
    'yahoo', 
    { 'tag': 'microsoft', 'host': [ 'msdn.com' ] }, 
    'twitter', 
    'zynga',
    
    'techcrunch', 
    'htc', 
    'amazon', 
    'mozilla', 
    'dell', 
    'nokia', 
    'novell', 
    'lenovo', 
    'nasa',
    
    'ubuntu', 
    'adobe', 
    'github', 
    'cisco', 
    'motorola', 
    'samsung', 
    'verizon', 
    { 'symbol': 'at&t', 'internal': 'atandt' },
    'sprint', 
    'tmobile',
    
    'instagram', 
    'square', 
    'stripe', 
    'anonymous', 
    'webkit', 
    'opera', 
    'tesla', 
    'redhat', 
    'centos',
    
    'gnu', 
    'mpaa', 
    'riaa', 
    'w3c', 
    'isohunt', 
    'obama', 
    'ifpi', 
    'nsa', 
    'cia', 
    'fbi', 
    'csis', 
    'wikileaks',
    
    'snowden', 
    'kde', 
    'gnome', 
    'comcast', 
    'fcc', 
    'china', 
    'usa', 
    'yale', 
    'navy', 
    'debian',
    
    'spacex', 
    'turing', 
    'mit', 
    'stanford', 
    'uber', 
    'lyft', 
    'hbo', 
    'sony', 
    'fdic', 
    'ucla', 
    'canada',
    
    'antarctica', 
    'arctic', 
    'tor', 
    'wolfram', 
    'mojang', 
    'dropbox',

    # Languages
    'php', 
    'javascript', 
    'java', 
    'perl', 
    'python', 
    'ruby', 
    'html', 
    'html5',
    'css', 
    { 'tag': 'css2', 'implies': 'css' }, 
    { 'tag': 'css3', 'implies': 'css' }, 
    'flash', 
    'lisp', 
    { 'tag': 'clojure', 'implies': 'lisp' }, 
    'racket', 
    'scheme',
    'arc',
    'scala', 
    'lua', 
    'haxe', 
    'ocaml', 
    'erlang', 
    'rust', 
    'ecmascript', 
    'haskell', 
    'nim',
    'prolog',
    { 'tag': 'go', 'alt': 'golang', 'internal': 'golang' }, 
    { 'tag': 'c', 'internal': 'clanguage' }, 
    { 'tag': 'd', 'internal': 'dlanguage' }, 
    { 'symbol': 'c++', 'internal': 'cplusplus' },
    { 'symbol': 'c#', 'internal': 'csharp' },
    { 'symbol': 'f#', 'internal': 'fsharp' },
    'swift',
    'nvidia',

    # Technologies
    'linux', 
    'bsd',
    'mongodb', 
    'cassandra', 
    'hadoop', 
    'android', 
    'node',
    'iphone', 
    'ipad', 
    'ipod', 
    'ec2', 
    'firefox', 
    'safari', 
    'servo',
    { 'tag': 'chrome', 'alt': 'chromium' }, 
    'windows', 
    { 'tag': 'mac', 'alt': 'macintosh' }, 
    'osx',
    'git', 
    'subversion', 
    'mercurial', 
    { 'tag': 'neovim', 'implies': 'vim' },
    'vim',
    { 'tag': 'vi', 'internal': 'vieditor' },
    'emacs', 
    'bitcoin', 
    'drupal', 
    'wordpress', 
    'unicode', 
    'pdf', 
    'wifi', 
    'phonegap', 
    'minecraft', 
    'svg', 
    'gif', 
    'png', 
    'dns', 
    'torrent',
    'docker', 
    'drone(s)', 
    'meteor', 
    'react', 
    { 'tag': 'openbsd', 'implies': 'bsd' }, 
    { 'tag': 'freebsd', 'implies': 'bsd' },
    'sass', 
    'scss', 
    'aes', 
    'rsa',
    { 'tag': 'ssl', 'implies': 'https' }, 
    { 'tag': 'tls', 'implies': 'https' }, 
    'http', 
    'https',
    'smtp', 
    'ftp', 
    'webrtc', 
    'pgp', 
    'gpg', 
    'ios', 
    'ssd', 
    'openssh', 
    'openssl',
    'bash', 
    'ksh', 
    'zsh', 
    { 'tag': 'jpeg', 'alt': 'jpg' },
    'dbus',
    'emoji',
    'mysql',
    { 'tag': 'postgresql', 'alt': 'postgres' },
    'json',
    'xml',
    'yaml',
    'csv',
    'arm',
    'mips',
    'gpu',
    'awk',
    'sed',
    'ssh',
    'grep',
    { 'tag': 'regex', 'alt': 'regexp' },
    'webgl',
    'glsl',
    { 'tag': 'gmail', 'implies': 'google' },

    # Frameworks
    'django', 
    'rails', 
    'jquery', 
    'prototype', 
    'mootools', 
    { 'tag': 'angular', 'alt': 'angularjs' },
    { 'tag': 'ember', 'alt': 'emberjs' }
]

TAGS = {}
SYMBOLS = {}
DISPLAY = {}
INTERNAL = {}

# Replaces a token that matches an internal's display token with the internal representation
def replaceInternal(tokens):
    return [INTERNAL[tag] if INTERNAL.has_key(tag) else tag for tag in tokens]

def displayTags(tags):
    return [DISPLAY[tag] if DISPLAY.has_key(tag) else tag for tag in tags]

def isSymbol(token):
    return SYMBOLS[token]['tags'][0] if SYMBOLS.has_key(token) else None

# Note that this may return duplicates
def extractTags(s):
    tags = []
    s = s.lower();
    for symbol in SYMBOLS.keys():
        if s.find(symbol) != -1:
            # Eat the symbol so we don't match on it any more
            s = s.replace(symbol, '')
            tags += SYMBOLS[symbol]['tags']

    for bit in re.split("[^A-Za-z0-9]+", s):
        if TAGS.has_key(bit):
            tags += TAGS[bit]['tags']

    return tags

for tag_entry in RAW_TAGS:
    if type(tag_entry) == str:
        tag_entry = { 'tag': tag_entry }

    symbol = tag_entry.has_key('symbol')
    if symbol:
        tag = tag_entry['symbol']
    else:
        tag = tag_entry['tag']
    output = {}

    # Reverse map
    if tag_entry.has_key('internal'):
        DISPLAY[tag_entry['internal']] = tag
        INTERNAL[tag] = tag_entry['internal']

    # plural?
    if tag.find('(s)') != -1:
        root = tag.replace('(s)', '')
        input = [ root, root + 's' ]
        output['tags'] = [ root ]
    else:
        input = [ tag ]
        if tag_entry.has_key('internal'):
            output['tags'] = [ tag_entry['internal'] ]
        else:
            output['tags'] = [ tag ]

    # implies adds additional output tags for a given input
    if tag_entry.has_key('implies'):
        implies = tag_entry['implies']
        if type(implies) == str:
            output['tags'] += [ implies ]
        else:
            output['tags'] += implies

    # alt adds addtional input tags for a given output
    if tag_entry.has_key('alt'):
        alt = tag_entry['alt']
        if type(alt) == str:
            input += [ alt ]
        else:
            for alt in tag_entry['alt']:
                if alt.find('(s)') != -1:
                    root = alt.replace('(s)', '')
                    input += [ alt, alt + 's' ]
                else:
                    input += [ alt ]

    if symbol:
        for tag in input:
            if SYMBOLS.has_key(tag):
                raise Exception('Duplicate symbol: ' + tag)
            SYMBOLS[tag] = output
    else:
        for tag in input:
            if TAGS.has_key(tag):
                raise Exception('Duplicate tag: ' + tag)
            TAGS[tag] = output


class TestTags(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(['rust'], extractTags("I love Rust!"))

    def test_plural(self):
        self.assertEqual(['video'], extractTags("Good old video"))
        self.assertEqual(['video'], extractTags("Good old videos"))

    def test_plural_dupe(self):
        self.assertEqual(set(['video']), set(extractTags("Good old video and videos")))

    def test_alt(self):
        self.assertEqual(['chrome'], extractTags("Chromium is a project"))
        self.assertEqual(['angular'], extractTags("AngularJS is fun"))

    def test_alt_dupe(self):
        self.assertEqual(set(['chrome']), set(extractTags("Chromium is the open Chrome")))

    def test_implies(self):
        self.assertEqual(['neovim', 'vim'], extractTags("Neovim is kind of cool"))

    def test_implies_dupe(self):
        self.assertEqual(set(['neovim', 'vim']), set(extractTags("Neovim is a kind of vim")))

    def test_internal(self):
        self.assertEqual(['clanguage'], extractTags("C is hard"))
        self.assertEqual(['dlanguage'], extractTags("D is hard"))

    def test_symbol(self):
        self.assertEqual(['csharp'], extractTags("C# is hard"))
        self.assertEqual(['cplusplus'], extractTags("C++ is hard"))
        self.assertEqual(['atandt'], extractTags("AT&T has an ampersand"))

if __name__ == '__main__':
    unittest.main()

