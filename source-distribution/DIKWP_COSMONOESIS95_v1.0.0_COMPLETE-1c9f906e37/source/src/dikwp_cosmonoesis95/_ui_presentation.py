"""Offline interface presentation. Project creator: Yucong Duan (段玉聪)."""
from html.parser import HTMLParser
import html, json, re

messages={'总览': 'Dashboard', '决策': 'Decision', '天': 'days', '外部行动权限': 'External action authority', '不确定': 'Uncertain', '修复': 'Repair', '权重': 'Weight', '模型退役': 'Model retirement', '世界模型权重': 'World-model weights', '模型': 'Model', '概念': 'Concept', '记忆': 'Memory', '主体边界': 'Actor boundary', '修订': 'Revision', '安全边界': 'Safety boundaries', '证书': 'Certificate', '说明': 'Notes', '能力': 'Capability', '类型': 'Type', '证据': 'Evidence', '主体': 'Party', '数量': 'Quantity', '地点': 'Location', '目的': 'Purpose', '授权': 'Authorization', '数据': 'Data', '边界：': 'Scope:', '可能不可逆': 'May be irreversible', '允许': 'Allowed', '生成': 'Generate', '世界': 'Scenario', '性质': 'Nature', '当前': 'Current', '目标': 'Target', '教育': 'Education', '审计': 'Audit', '当前证据': 'Current evidence', '决定': 'Decision', '对象': 'Object', '置信': 'Confidence', '通道': 'Channel', '概率': 'Probability', '解释': 'Interpretation', '状态': 'Status', '方法边界': 'Method scope', '自动外部行动权': 'Automatic external action authority', '公开': 'Public', '现实结果': 'Observed outcome', '宇宙意识 · 世界宗教与文明 DIKWP 归一 · 非规范主张审计 · 多世界模型 · 现实接触与责任闭环': 'Cosmic consciousness · DIKWP mapping of religions and civilizations · Claim audits · Multiple models · Evidence and responsibility', '坐标统一，不设空间外残差': 'Shared coordinates with explicit extensions for unknown concepts', '36个传统 · 13个文明语义群': '36 traditions · 13 civilizational semantic groups', '15个意识理论 · 7个宇宙模型': '15 consciousness theories · 7 cosmological models', '自动外部行动权限 0': 'Automatic external action authority: 0', '开放终极定义': 'An open definition of ultimate inquiry', '终极不是最后权威，而是把来源、模型竞争、反证、价值、目的、现实返回、权利和可修订性纳入同一闭环。所有宗教、文明、科学和哲学概念进入统一 DIKWP 空间；归一不等于历史同一。': 'The framework places sources, competing models, counterevidence, values, purpose, outcomes, rights and revision in one review cycle. A shared DIKWP representation does not make religious, civilizational, scientific or philosophical concepts historically identical.', 'DIKWP 统一语义空间': 'Shared DIKWP semantic space', '宗教与哲学传统': 'Religious and philosophical traditions', '搜索传统、术语、目的或坐标…': 'Search traditions, terms, purposes or coordinates…', '传统': 'Tradition', '原生概念': 'Original concept', '目的／意识映射': 'Purpose or consciousness mapping', '主要坐标': 'Main coordinates', '文明语义群': 'Civilizational semantic group', '概念归一结果': 'Concept-mapping results', '此离线仪表盘展示已编译概念。命令行可归一任意新概念。': 'This offline dashboard displays compiled concepts. The command-line tool accepts additional concepts.', '统一空间原则': 'Shared-space principle', '不存在永久的空间外不可互译区。未知概念通过版本化的 DIKWP 子坐标扩展；低置信度要求更多语境。': 'The framework extends versioned DIKWP subcoordinates for unknown concepts and requests more context where confidence is low, rather than treating a concept as permanently untranslatable.', '相似向量只说明结构接近，不证明神学、历史或物理对象完全相同。': 'Similar vectors indicate structural resemblance; they do not establish theological, historical or physical identity.', '非规范材料审计': 'Noncanonical-material audit', '主张': 'Claim', '风险': 'Risk', '发现': 'Findings', '修正': 'Correction', '意识候选多模型评估': 'Multiple-model assessment of consciousness candidates', '宇宙意识七世界模型': 'Seven models of cosmic consciousness', '宇宙／外星主体接触协议': 'Cosmic or extraterrestrial contact protocol', '示例模型竞争': 'Competing example models', '开放终极工作规律': 'Open working principles', '路线': 'Route', '版本：': 'Version:', '操作': 'Actions', '目的与边界': 'Purpose and scope', '观察者': 'Observer', '模式': 'Mode', '治理': 'Governance', '假设': 'Hypothesis', '证据缺口': 'Evidence gaps', '周期': 'Period', '闭环': 'Closure', '生命力': 'Vitality', '碳基': 'Carbon-based', '共同体': 'Community', '情境': 'Context', '未知': 'Unknown', '扩大': 'Expanding', '稳定': 'Stable', '依赖': 'Dependence', '载体': 'Entity', '候选系统': 'Candidate systems', '系统': 'System', '结构': 'Structure', '蚁群': 'Ant colony', '系统边界': 'System boundaries', '内容': 'Content', '领域': 'Domain', '一般': 'General', '健康': 'Health', '关系': 'Relationships', '建议': 'Advice', '对照': 'Control', '维度': 'Dimension', '主要风险': 'Main risks', '假说': 'Hypothesis', '复现': 'Reproduce', '来源': 'Source', '层级': 'Layer', '问题': 'Question', '边界': 'Scope', '家庭': 'Household', '事件': 'Event'}
normalized={re.sub(r"\s+"," ",k.strip()):v for k,v in messages.items()}
runtime="/* Interface localization. Creator: Yucong Duan (段玉聪). */\n(() => {\n  'use strict';\n  const configuration = document.getElementById('yd-interface-config');\n  if (!configuration) return;\n  const config = JSON.parse(configuration.textContent);\n  const dictionary = new Map(Object.entries(config.messages || {}).map(([a, b]) => [a.trim().replace(/\\s+/g, ' '), b]));\n  const numeric = /\\d[\\d,]*(?:\\.\\d+)?/g;\n  const templates = [];\n  const escapePattern = value => value.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');\n  for (const [source, target] of dictionary) {\n    const a = source.match(numeric) || [], b = target.match(numeric) || [];\n    if (!a.length || a.length > 12 || a.length !== b.length || !a.every((v, i) => v.replace(/,/g, '') === b[i].replace(/,/g, ''))) continue;\n    const parts = source.split(numeric);\n    templates.push({pattern: new RegExp('^' + parts.map(escapePattern).join('(\\\\d[\\\\d,]*(?:\\\\.\\\\d+)?)') + '$'), parts: target.split(numeric)});\n  }\n  const textState = new WeakMap();\n  const attributeState = new WeakMap();\n  const attributes = ['title', 'placeholder', 'aria-label', 'alt', 'label'];\n  const excluded = 'script,style,pre,code,textarea,[contenteditable],[data-source-language],[data-project-creator]';\n  let language = 'en';\n  const originalTitle = document.title;\n\n  function translate(value) {\n    const key = value.trim().replace(/\\s+/g, ' ');\n    let translated = dictionary.get(key);\n    if (translated === undefined && /[\\u3400-\\u9fff]/.test(key)) {\n      for (const template of templates) {\n        const match = key.match(template.pattern);\n        if (!match) continue;\n        translated = template.parts.map((part, i) => part + (match[i + 1] || '')).join('');\n        break;\n      }\n    }\n    if (translated === undefined) return value;\n    const leading = value.match(/^\\s*/)[0];\n    const trailing = value.match(/\\s*$/)[0];\n    return leading + translated + trailing;\n  }\n\n  function updateText(node) {\n    const parent = node.parentElement;\n    if (!parent || parent.closest(excluded)) return;\n    let saved = textState.get(node);\n    const current = node.nodeValue;\n    if (!saved || current !== saved.rendered) saved = { original: current, rendered: current };\n    const next = language === 'en' ? translate(saved.original) : saved.original;\n    if (next !== current) {\n      // Translating an option label must not change the value used by the application.\n      if (parent.tagName === 'OPTION' && !parent.hasAttribute('value')) parent.setAttribute('value', parent.textContent);\n      node.nodeValue = next;\n    }\n    saved.rendered = next;\n    textState.set(node, saved);\n  }\n\n  function updateAttributes(element) {\n    if (!element || element.closest(excluded)) return;\n    let saved = attributeState.get(element);\n    if (!saved) { saved = new Map(); attributeState.set(element, saved); }\n    for (const name of attributes) {\n      if (!element.hasAttribute(name)) continue;\n      // The label attribute is an interface label on these elements only.\n      if (name === 'label' && !['OPTION', 'OPTGROUP', 'TRACK'].includes(element.tagName)) continue;\n      const current = element.getAttribute(name);\n      let prior = saved.get(name);\n      if (!prior || current !== prior.rendered) prior = { original: current, rendered: current };\n      const next = language === 'en' ? translate(prior.original) : prior.original;\n      if (next !== current) element.setAttribute(name, next);\n      prior.rendered = next; saved.set(name, prior);\n    }\n  }\n\n  function visit(root) {\n    if (root.nodeType === Node.TEXT_NODE) { updateText(root); return; }\n    if (root.nodeType !== Node.ELEMENT_NODE || root.closest(excluded)) return;\n    updateAttributes(root);\n    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);\n    while (walker.nextNode()) updateText(walker.currentNode);\n    for (const element of root.querySelectorAll('[title],[placeholder],[aria-label],[alt],[label]')) updateAttributes(element);\n  }\n\n  function setLanguage(next) {\n    language = next === 'zh' ? 'zh' : 'en';\n    document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';\n    document.title = language === 'en' ? translate(originalTitle) : originalTitle;\n    visit(document.body);\n  }\n\n  function start() {\n    const select = config.nativeSelect ? document.querySelector(config.nativeSelect) : null;\n    const button = config.nativeButton ? document.querySelector(config.nativeButton) : null;\n    if (select) language = select.value === 'zh' ? 'zh' : 'en';\n    else if (config.storageKey) {\n      try { language = localStorage.getItem(config.storageKey) === 'zh' ? 'zh' : 'en'; } catch (_) { language = 'en'; }\n    }\n    setLanguage(language);\n    if (select) select.addEventListener('change', () => setLanguage(select.value));\n    if (button) button.addEventListener('click', () => setLanguage(language === 'en' ? 'zh' : 'en'));\n    const observer = new MutationObserver(records => {\n      for (const record of records) {\n        if (record.type === 'characterData') updateText(record.target);\n        else if (record.type === 'attributes') updateAttributes(record.target);\n        else for (const node of record.addedNodes) visit(node);\n      }\n    });\n    observer.observe(document.body, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: attributes });\n  }\n\n  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });\n  else start();\n})();\n"

def english(text):
    key=re.sub(r'\s+',' ',html.unescape(text).strip())
    if key not in normalized:return text
    leading=re.match(r'^\s*',text).group();trailing=re.search(r'\s*$',text).group()
    return leading+html.escape(normalized[key],quote=False)+trailing

class Surface(HTMLParser):
    def __init__(self,text,static=True):
        super().__init__(convert_charrefs=False);self.source=text;self.static=static;self.lines=[0]
        for m in re.finditer('\n',text):self.lines.append(m.end())
        self.stack=[];self.changes=[];self.credit=False;self.author=False;self.body_end=None
    def pos(self):
        row,col=self.getpos();return self.lines[row-1]+col
    def blocked(self):return any(t in ['script','style','pre','code','textarea','option'] for t in self.stack)
    def handle_starttag(self,tag,attrs):
        start=self.pos();raw=self.get_starttag_text();values=dict(attrs)
        if tag=='html':
            if re.search(r'\blang\s*=',raw,re.I):new=re.sub(r'(\blang\s*=\s*)([\"\']).*?\2',r'\1"en"',raw,count=1,flags=re.I)
            else:new=raw[:-1]+' lang="en">'
            self.changes.append((start,start+len(raw),new))
        elif tag=='meta' and (values.get('name') or '').lower()=='author':self.author=True
        if self.static and not self.blocked() and tag not in ['script','style']:
            new=raw
            for name in ['title','placeholder','aria-label','alt','label']:
                value=values.get(name)
                if not value:continue
                key=re.sub(r'\s+',' ',value.strip())
                if key not in normalized:continue
                escaped=html.escape(normalized[key],quote=True)
                new=re.sub(r'(\b'+re.escape(name)+r'\s*=\s*)([\"\'])(.*?)\2',lambda m:m.group(1)+m.group(2)+escaped+m.group(2),new,count=1,flags=re.I|re.S)
            if new!=raw:self.changes.append((start,start+len(raw),new))
        if tag not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(tag)
    def handle_endtag(self,tag):
        if tag=='h1' and not self.blocked() and not self.credit:
            p=self.pos()+len('</h1>');self.changes.append((p,p,'\n<p data-project-creator="true" style="font-size:.9rem;line-height:1.5;opacity:.85;margin:.5rem 0 1rem">Project creator: Yucong Duan (段玉聪).</p>'));self.credit=True
        if tag=='head' and not self.author:
            p=self.pos();self.changes.append((p,p,'<meta name="author" content="Yucong Duan (段玉聪)">\n'));self.author=True
        if tag=='body':self.body_end=self.pos()
        if tag in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
    def handle_data(self,data):
        if self.static and not self.blocked():
            replacement=english(data)
            if replacement!=data:
                start=self.pos();self.changes.append((start,start+len(data),replacement))

def localize_html(value):
    """Localize an HTML document; preserve other output formats exactly."""
    if not isinstance(value,str) or not re.match(r'\s*(?:<!doctype[^>]*>\s*)?<html\b',value,re.I):
        return value
    if 'data-project-creator="true"' in value or 'id="yd-interface-config"' in value:
        return value
    parser=Surface(value,static=True);parser.feed(value)
    changes=parser.changes
    at=parser.body_end if parser.body_end is not None else len(value)
    if messages:
        payload=json.dumps({'messages':messages},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
        addition='\n<script id="yd-interface-config" type="application/json">'+payload+'</script>\n<script>\n'+runtime+'\n</script>\n'
        changes.append((at,at,addition))
    if not parser.credit:
        changes.append((at,at,'\n<p data-project-creator="true">Project creator: Yucong Duan (段玉聪).</p>\n'))
    for start,end,text in sorted(changes,key=lambda x:(x[0],x[1]),reverse=True):
        value=value[:start]+text+value[end:]
    return value
