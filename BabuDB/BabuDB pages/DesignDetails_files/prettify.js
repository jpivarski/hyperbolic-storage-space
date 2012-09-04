/*
 Copyright (C) 2006 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
var b=!0,l=null,w=!1;window.PR_SHOULD_USE_CONTINUATION=b;window.PR_TAB_WIDTH=8;window.PR_normalizedHtml=window.PR=window.prettyPrintOne=window.prettyPrint=void 0;window._pr_isIE6=function(){var a=navigator&&navigator.userAgent&&navigator.userAgent.match(/\bMSIE ([678])\./),a=a?+a[1]:w;window._pr_isIE6=function(){return a};return a};
var H=function(a){return a.replace(x,"&amp;").replace(y,"&lt;").replace(C,"&gt;")},M=function(a,g,h){switch(a.nodeType){case 1:var k=a.tagName.toLowerCase();g.push("<",k);var d=a.attributes,n=d.length;if(n){if(h){for(var i=[],o=n;0<=--o;)i[o]=d[o];i.sort(function(a,g){return a.name<g.name?-1:a.name===g.name?0:1});d=i}for(o=0;o<n;++o)i=d[o],i.specified&&g.push(" ",i.name.toLowerCase(),'="',i.value.replace(x,"&amp;").replace(y,"&lt;").replace(C,"&gt;").replace(aa,"&quot;"),'"')}g.push(">");for(d=a.firstChild;d;d=
d.nextSibling)M(d,g,h);(a.firstChild||!/^(?:br|link|img)$/.test(k))&&g.push("</",k,">");break;case 3:case 4:g.push(H(a.nodeValue))}},N=function(a){function g(a){if("\\"!==a.charAt(0))return a.charCodeAt(0);switch(a.charAt(1)){case "b":return 8;case "t":return 9;case "n":return 10;case "v":return 11;case "f":return 12;case "r":return 13;case "u":case "x":return parseInt(a.substring(2),16)||a.charCodeAt(1);case "0":case "1":case "2":case "3":case "4":case "5":case "6":case "7":return parseInt(a.substring(1),
8);default:return a.charCodeAt(1)}}function h(a){if(32>a)return(16>a?"\\x0":"\\x")+a.toString(16);a=String.fromCharCode(a);if("\\"===a||"-"===a||"["===a||"]"===a)a="\\"+a;return a}function k(a){for(var f=a.substring(1,a.length-1).match(RegExp("\\\\u[0-9A-Fa-f]{4}|\\\\x[0-9A-Fa-f]{2}|\\\\[0-3][0-7]{0,2}|\\\\[0-7]{1,2}|\\\\[\\s\\S]|-|[^-\\\\]","g")),a=[],c=[],k="^"===f[0],e=k?1:0,u=f.length;e<u;++e){var j=f[e];switch(j){case "\\B":case "\\b":case "\\D":case "\\d":case "\\S":case "\\s":case "\\W":case "\\w":a.push(j);
continue}var j=g(j),d;e+2<u&&"-"===f[e+1]?(d=g(f[e+2]),e+=2):d=j;c.push([j,d]);65>d||122<j||(65>d||90<j||c.push([Math.max(65,j)|32,Math.min(d,90)|32]),97>d||122<j||c.push([Math.max(97,j)&-33,Math.min(d,122)&-33]))}c.sort(function(a,c){return a[0]-c[0]||c[1]-a[1]});f=[];j=[NaN,NaN];for(e=0;e<c.length;++e)u=c[e],u[0]<=j[1]+1?j[1]=Math.max(j[1],u[1]):f.push(j=u);c=["["];k&&c.push("^");c.push.apply(c,a);for(e=0;e<f.length;++e)u=f[e],c.push(h(u[0])),u[1]>u[0]&&(u[1]+1>u[0]&&c.push("-"),c.push(h(u[1])));
c.push("]");return c.join("")}function d(a){for(var f=a.source.match(RegExp("(?:\\[(?:[^\\x5C\\x5D]|\\\\[\\s\\S])*\\]|\\\\u[A-Fa-f0-9]{4}|\\\\x[A-Fa-f0-9]{2}|\\\\[0-9]+|\\\\[^ux0-9]|\\(\\?[:!=]|[\\(\\)\\^]|[^\\x5B\\x5C\\(\\)\\^]+)","g")),c=f.length,g=[],e=0,d=0;e<c;++e){var j=f[e];"("===j?++d:"\\"===j.charAt(0)&&(j=+j.substring(1))&&j<=d&&(g[j]=-1)}for(e=1;e<g.length;++e)-1===g[e]&&(g[e]=++n);for(d=e=0;e<c;++e)j=f[e],"("===j?(++d,void 0===g[d]&&(f[e]="(?:")):"\\"===j.charAt(0)&&(j=+j.substring(1))&&
j<=d&&(f[e]="\\"+g[d]);for(d=e=0;e<c;++e)"^"===f[e]&&"^"!==f[e+1]&&(f[e]="");if(a.ignoreCase&&i)for(e=0;e<c;++e)j=f[e],a=j.charAt(0),2<=j.length&&"["===a?f[e]=k(j):"\\"!==a&&(f[e]=j.replace(/[a-zA-Z]/g,function(a){a=a.charCodeAt(0);return"["+String.fromCharCode(a&-33,a|32)+"]"}));return f.join("")}for(var n=0,i=w,o=w,p=0,m=a.length;p<m;++p){var q=a[p];if(q.ignoreCase)o=b;else if(/[a-z]/i.test(q.source.replace(/\\u[0-9a-f]{4}|\\x[0-9a-f]{2}|\\[^ux]/gi,""))){i=b;o=w;break}}for(var t=[],p=0,m=a.length;p<
m;++p){q=a[p];if(q.global||q.multiline)throw Error(""+q);t.push("(?:"+d(q)+")")}return RegExp(t.join("|"),o?"gi":"g")},O=function(a,g,h,k){g&&(a={source:g,basePos:a},h(a),k.push.apply(k,a.decorations))},R=function(a,g){for(var h={},k,d=a.concat(g),n=[],i={},o=0,p=d.length;o<p;++o){var m=d[o],q=m[3];if(q)for(var t=q.length;0<=--t;)h[q.charAt(t)]=m;m=m[1];q=""+m;i.hasOwnProperty(q)||(n.push(m),i[q]=l)}n.push(/[\0-\uffff]/);k=N(n);var z=g.length,f=function(a){for(var d=a.source,e=a.basePos,m=[e,"pln"],
j=0,d=d.match(k)||[],t={},o=0,n=d.length;o<n;++o){var i=d[o],p=t[i],q=void 0,r;if("string"===typeof p)r=w;else{var s=h[i.charAt(0)];if(s)q=i.match(s[1]),p=s[0];else{for(r=0;r<z;++r)if(s=g[r],q=i.match(s[1])){p=s[0];break}q||(p="pln")}if((r=5<=p.length&&"lang-"===p.substring(0,5))&&!(q&&"string"===typeof q[1]))r=w,p="src";r||(t[i]=p)}s=j;j+=i.length;if(r){r=q[1];var A=i.indexOf(r),v=A+r.length;q[2]&&(v=i.length-q[2].length,A=v-r.length);p=p.substring(5);O(e+s,i.substring(0,A),f,m);O(e+s+A,r,P(p,r),
m);O(e+s+v,i.substring(v),f,m)}else m.push(e+s,p)}a.decorations=m};return f},S=function(a){var g=[],h=[];a.tripleQuotedStrings?g.push(["str",/^(?:\'\'\'(?:[^\'\\]|\\[\s\S]|\'{1,2}(?=[^\']))*(?:\'\'\'|$)|\"\"\"(?:[^\"\\]|\\[\s\S]|\"{1,2}(?=[^\"]))*(?:\"\"\"|$)|\'(?:[^\\\']|\\[\s\S])*(?:\'|$)|\"(?:[^\\\"]|\\[\s\S])*(?:\"|$))/,l,"'\""]):a.multiLineStrings?g.push(["str",/^(?:\'(?:[^\\\']|\\[\s\S])*(?:\'|$)|\"(?:[^\\\"]|\\[\s\S])*(?:\"|$)|\`(?:[^\\\`]|\\[\s\S])*(?:\`|$))/,l,"'\"`"]):g.push(["str",/^(?:\'(?:[^\\\'\r\n]|\\.)*(?:\'|$)|\"(?:[^\\\"\r\n]|\\.)*(?:\"|$))/,
l,"\"'"]);a.verbatimStrings&&h.push(["str",/^@\"(?:[^\"]|\"\")*(?:\"|$)/,l]);var k=a.hashComments;k&&(a.cStyleComments?(1<k?g.push(["com",/^#(?:##(?:[^#]|#(?!##))*(?:###|$)|.*)/,l,"#"]):g.push(["com",/^#(?:(?:define|elif|else|endif|error|ifdef|include|ifndef|line|pragma|undef|warning)\b|[^\r\n]*)/,l,"#"]),h.push(["str",/^<(?:(?:(?:\.\.\/)*|\/?)(?:[\w-]+(?:\/[\w-]+)+)?[\w-]+\.h|[a-z]\w*)>/,l])):g.push(["com",/^#[^\r\n]*/,l,"#"]));a.cStyleComments&&(h.push(["com",/^\/\/[^\r\n]*/,l]),h.push(["com",/^\/\*[\s\S]*?(?:\*\/|$)/,
l]));a.regexLiterals&&h.push(["lang-regex",RegExp("^"+ga+"(/(?=[^/*])(?:[^/\\x5B\\x5C]|\\x5C[\\s\\S]|\\x5B(?:[^\\x5C\\x5D]|\\x5C[\\s\\S])*(?:\\x5D|$))+/)")]);a=a.keywords.replace(/^\s+|\s+$/g,"");a.length&&h.push(["kwd",RegExp("^(?:"+a.replace(/\s+/g,"|")+")\\b"),l]);g.push(["pln",/^\s+/,l," \r\n\t\u00a0"]);h.push(["lit",/^@[a-z_$][a-z_$@0-9]*/i,l],["typ",/^@?[A-Z]+[a-z][A-Za-z_$@0-9]*/,l],["pln",/^[a-z_$][a-z_$@0-9]*/i,l],["lit",/^(?:0x[a-f0-9]+|(?:\d(?:_\d+)*\d*(?:\.\d*)?|\.\d\+)(?:e[+\-]?\d+)?)[a-z]*/i,
l,"0123456789"],["pun",/^.[^\s\w\.$@\'\"\`\/\#]*/,l]);return R(g,h)},U=function(a,g){for(var h=g.length;0<=--h;){var k=g[h];T.hasOwnProperty(k)?"console"in window&&console.warn("cannot override language handler %s",k):T[k]=a}},P=function(a,g){if(!a||!T.hasOwnProperty(a))a=/^\s*</.test(g)?"default-markup":"default-code";return T[a]},sa=function(a){var g=a.sourceCodeHtml,h=a.langExtension;a.prettyPrintedHtml=g;try{var k,d=g.match(ha),g=[],n=0,i=[];if(d)for(var o=0,p=d.length;o<p;++o){var m=d[o];if(1<
m.length&&"<"===m.charAt(0)){if(!ia.test(m))if(ja.test(m))g.push(m.substring(9,m.length-3)),n+=m.length-12;else if(ka.test(m))g.push("\n"),++n;else if(0<=m.indexOf("nocode")&&m.replace(/\s(\w+)\s*=\s*(?:\"([^\"]*)\"|'([^\']*)'|(\S+))/g,' $1="$2$3$4"').match(/[cC][lL][aA][sS][sS]=\"[^\"]*\bnocode\b/)){var q=m.match(la)[2],t=1,z;z=o+1;a:for(;z<p;++z){var f=d[z].match(la);if(f&&f[2]===q)if("/"===f[1]){if(0===--t)break a}else++t}z<p?(i.push(n,d.slice(o,z+1).join("")),o=z):i.push(n,m)}else i.push(n,m)}else{var c;
var t=m,B=t.indexOf("&");if(0>B)c=t;else{for(--B;0<=(B=t.indexOf("&#",B+1));){var e=t.indexOf(";",B);if(0<=e){var u=t.substring(B+3,e),j=10;u&&"x"===u.charAt(0)&&(u=u.substring(1),j=16);var W=parseInt(u,j);isNaN(W)||(t=t.substring(0,B)+String.fromCharCode(W)+t.substring(e+1))}}c=t.replace(ma,"<").replace(na,">").replace(oa,"'").replace(pa,'"').replace(qa," ").replace(ra,"&")}g.push(c);n+=c.length}}k={source:g.join(""),tags:i};var X=k.source;a.source=X;a.basePos=0;a.extractedTags=k.tags;P(h,X)(a);
var h=function(a){if(a>A){v&&v!==I&&(s.push("</span>"),v=l);!v&&I&&(v=I,s.push('<span class="',v,'">'));var c=H(ba(Y.substring(A,a))).replace(ca?ua:va,"$1&#160;");ca=wa.test(c);s.push(c.replace(xa,Q));A=a}},Y=a.source,F=a.extractedTags,D=a.decorations,G=a.numberLines,r=a.sourceNode,s=[],A=0,v=l,I=l,d=k=0,ba,da=window.PR_TAB_WIDTH,E=0;ba=function(a){for(var c=l,d=0,e=0,f=a.length;e<f;++e){var g=a.charAt(e);switch(g){case "\t":c||(c=[]);c.push(a.substring(d,e));d=da-E%da;for(E+=d;0<=d;d-=16)c.push("                ".substring(0,
d));d=e+1;break;case "\n":E=0;break;default:++E}}if(!c)return a;c.push(a.substring(d));return c.join("")};var va=/([\r\n ]) /g,ua=/(^| ) /gm,xa=/\r\n?|\n/g,wa=/[ \r\n]$/,ca=b,J=window._pr_isIE6(),ea=J?r&&"PRE"===r.tagName?6===J?"&#160;\r\n":7===J?"&#160;<br />\r":8===J?"&#160;<br />":"&#160;\r":"&#160;<br />":"<br />",Q;if(G){for(var fa=[],r=0;10>r;++r)fa[r]=ea+'</li><li class="L'+r+'">';var K="number"===typeof G?G-1:0;s.push('<ol class="linenums"><li class="L',K%10,'"');K&&s.push(' value="',K+1,
'"');s.push(">");Q=function(){var a=fa[++K%10];return v?"</span>"+a+'<span class="'+v+'">':a}}else Q=ea;for(;;){var ya;if(ya=k<F.length?d<D.length?F[k]<=D[d]:b:w)h(F[k]),v&&(s.push("</span>"),v=l),s.push(F[k+1]),k+=2;else if(d<D.length)h(D[d]),I=D[d+1],d+=2;else break}h(Y.length);v&&s.push("</span>");G&&s.push("</li></ol>");a.prettyPrintedHtml=s.join("")}catch(L){"console"in window&&console.log(L&&L.stack?L.stack:L)}},ta=function(a,g,h){a={sourceCodeHtml:a,langExtension:g,numberLines:h};sa(a);return a.prettyPrintedHtml},
Aa=function(a){function g(){for(var d=window.PR_SHOULD_USE_CONTINUATION?o.now()+250:Infinity;p<k.length&&o.now()<d;p++){var h=k[p];if(h.className&&0<=h.className.indexOf("prettyprint")){var i=h.className.match(/\blang-(\w+)\b/);i&&(i=i[1]);for(var f=w,c=h.parentNode;c;c=c.parentNode)if(("pre"===c.tagName||"code"===c.tagName||"xmp"===c.tagName)&&c.className&&0<=c.className.indexOf("prettyprint")){f=b;break}if(!f){c=h;l===V&&(f=document.createElement("PRE"),f.appendChild(document.createTextNode('<!DOCTYPE foo PUBLIC "foo bar">\n<foo />')),
V=!/</.test(f.innerHTML));if(V)if(f=c.innerHTML,"XMP"===c.tagName)f=H(f);else{if("PRE"===c.tagName||!za.test(f))c=b;else{var n="";c.currentStyle?n=c.currentStyle.whiteSpace:window.getComputedStyle&&(n=window.getComputedStyle(c,l).whiteSpace);c=!n||"pre"===n}c||(f=f.replace(/(<br\s*\/?>)[\r\n]+/g,"$1").replace(/(?:[\r\n]+[ \t]*)+/g," "))}else{f=[];for(c=c.firstChild;c;c=c.nextSibling)M(c,f);f=f.join("")}f=f.replace(/(?:\r\n?|\n)$/,"");c=h.className.match(/\blinenums\b(?::(\d+))?/);m={sourceCodeHtml:f,
langExtension:i,sourceNode:h,numberLines:c?c[1]&&c[1].length?+c[1]:b:w};sa(m);if(h=m.prettyPrintedHtml)if(i=m.sourceNode,"XMP"===i.tagName){f=document.createElement("PRE");for(c=0;c<i.attributes.length;++c)if(n=i.attributes[c],n.specified){var e=n.name.toLowerCase();"class"===e?f.className=n.value:f.setAttribute(n.name,n.value)}f.innerHTML=h;i.parentNode.replaceChild(f,i)}else i.innerHTML=h}}}p<k.length?setTimeout(g,250):a&&a()}for(var h=[document.getElementsByTagName("pre"),document.getElementsByTagName("code"),
document.getElementsByTagName("xmp")],k=[],d=0;d<h.length;++d)for(var n=0,i=h[d].length;n<i;++n)k.push(h[d][n]);var h=l,o=Date;o.now||(o={now:function(){return(new Date).getTime()}});var p=0,m;g()},Ba,Ca="! != !== # % %= & && &&= &= ( * *= += , -= -> / /= : :: ; < << <<= <= = == === > >= >> >>= >>> >>>= ? @ [ ^ ^= ^^ ^^= { | |= || ||= ~ break case continue delete do else finally instanceof return throw try typeof".split(" "),Z="(?:^^|[+-]",$=0;
for(;$<Ca.length;++$)Z+="|"+Ca[$].replace(/([^=<>:&a-z])/g,"\\$1");
var ga=Ba=Z+=")\\s*",x=/&/g,y=/</g,C=/>/g,aa=/\"/g,ma=/&lt;/g,na=/&gt;/g,oa=/&apos;/g,pa=/&quot;/g,ra=/&amp;/g,qa=/&nbsp;/g,za=/[\r\n]/g,V=l,ha=RegExp("[^<]+|<\!--[\\s\\S]*?--\>|<!\\[CDATA\\[[\\s\\S]*?\\]\\]>|</?[a-zA-Z](?:[^>\"']|'[^']*'|\"[^\"]*\")*>|<","g"),ia=/^<\!--/,ja=/^<!\[CDATA\[/,ka=/^<br\b/i,la=/^<(\/?)([a-zA-Z][a-zA-Z0-9]*)/,Da=S({keywords:"break continue do else for if return while auto case char const default double enum extern float goto int long register short signed sizeof static struct switch typedef union unsigned void volatile catch class delete false import new operator private protected public this throw true try typeof alignof align_union asm axiom bool concept concept_map const_cast constexpr decltype dynamic_cast explicit export friend inline late_check mutable namespace nullptr reinterpret_cast static_assert static_cast template typeid typename using virtual wchar_t where break continue do else for if return while auto case char const default double enum extern float goto int long register short signed sizeof static struct switch typedef union unsigned void volatile catch class delete false import new operator private protected public this throw true try typeof abstract boolean byte extends final finally implements import instanceof null native package strictfp super synchronized throws transient as base by checked decimal delegate descending dynamic event fixed foreach from group implicit in interface internal into is lock object out override orderby params partial readonly ref sbyte sealed stackalloc string select uint ulong unchecked unsafe ushort var break continue do else for if return while auto case char const default double enum extern float goto int long register short signed sizeof static struct switch typedef union unsigned void volatile catch class delete false import new operator private protected public this throw true try typeof debugger eval export function get null set undefined var with Infinity NaN caller delete die do dump elsif eval exit foreach for goto if import last local my next no our print package redo require sub undef unless until use wantarray while BEGIN END break continue do else for if return while and as assert class def del elif except exec finally from global import in is lambda nonlocal not or pass print raise try with yield False True None break continue do else for if return while alias and begin case class def defined elsif end ensure false in module next nil not or redo rescue retry self super then true undef unless until when yield BEGIN END break continue do else for if return while case done elif esac eval fi function in local set then until ",hashComments:b,
cStyleComments:b,multiLineStrings:b,regexLiterals:b}),T={};U(Da,["default-code"]);U(R([],[["pln",/^[^<?]+/],["dec",/^<!\w[^>]*(?:>|$)/],["com",/^<\!--[\s\S]*?(?:-\->|$)/],["lang-",/^<\?([\s\S]+?)(?:\?>|$)/],["lang-",/^<%([\s\S]+?)(?:%>|$)/],["pun",/^(?:<[%?]|[%?]>)/],["lang-",/^<xmp\b[^>]*>([\s\S]+?)<\/xmp\b[^>]*>/i],["lang-js",/^<script\b[^>]*>([\s\S]*?)(<\/script\b[^>]*>)/i],["lang-css",/^<style\b[^>]*>([\s\S]*?)(<\/style\b[^>]*>)/i],["lang-in.tag",/^(<\/?[a-z][^<>]*>)/i]]),"default-markup htm html mxml xhtml xml xsl".split(" "));
U(R([["pln",/^[\s]+/,l," \t\r\n"],["atv",/^(?:\"[^\"]*\"?|\'[^\']*\'?)/,l,"\"'"]],[["tag",/^^<\/?[a-z](?:[\w.:-]*\w)?|\/?>$/i],["atn",/^(?!style[\s=]|on)[a-z](?:[\w:-]*\w)?/i],["lang-uq.val",/^=\s*([^>\'\"\s]*(?:[^>\'\"\s\/]|\/(?=\s)))/],["pun",/^[=<>\/]+/],["lang-js",/^on\w+\s*=\s*\"([^\"]+)\"/i],["lang-js",/^on\w+\s*=\s*\'([^\']+)\'/i],["lang-js",/^on\w+\s*=\s*([^\"\'>\s]+)/i],["lang-css",/^style\s*=\s*\"([^\"]+)\"/i],["lang-css",/^style\s*=\s*\'([^\']+)\'/i],["lang-css",/^style\s*=\s*([^\"\'>\s]+)/i]]),
["in.tag"]);U(R([],[["atv",/^[\s\S]+/]]),["uq.val"]);
U(S({keywords:"break continue do else for if return while auto case char const default double enum extern float goto int long register short signed sizeof static struct switch typedef union unsigned void volatile catch class delete false import new operator private protected public this throw true try typeof alignof align_union asm axiom bool concept concept_map const_cast constexpr decltype dynamic_cast explicit export friend inline late_check mutable namespace nullptr reinterpret_cast static_assert static_cast template typeid typename using virtual wchar_t where ",hashComments:b,
cStyleComments:b}),"c cc cpp cxx cyc m".split(" "));U(S({keywords:"null true false"}),["json"]);
U(S({keywords:"break continue do else for if return while auto case char const default double enum extern float goto int long register short signed sizeof static struct switch typedef union unsigned void volatile catch class delete false import new operator private protected public this throw true try typeof abstract boolean byte extends final finally implements import instanceof null native package strictfp super synchronized throws transient as base by checked decimal delegate descending dynamic event fixed foreach from group implicit in interface internal into is lock object out override orderby params partial readonly ref sbyte sealed stackalloc string select uint ulong unchecked unsafe ushort var ",hashComments:b,
cStyleComments:b,verbatimStrings:b}),["cs"]);
U(S({keywords:"break continue do else for if return while auto case char const default double enum extern float goto int long register short signed sizeof static struct switch typedef union unsigned void volatile catch class delete false import new operator private protected public this throw true try typeof abstract boolean byte extends final finally implements import instanceof null native package strictfp super synchronized throws transient ",cStyleComments:b}),["java"]);
U(S({keywords:"break continue do else for if return while case done elif esac eval fi function in local set then until ",hashComments:b,multiLineStrings:b}),["bsh","csh","sh"]);U(S({keywords:"break continue do else for if return while and as assert class def del elif except exec finally from global import in is lambda nonlocal not or pass print raise try with yield False True None ",hashComments:b,multiLineStrings:b,tripleQuotedStrings:b}),["cv","py"]);
U(S({keywords:"caller delete die do dump elsif eval exit foreach for goto if import last local my next no our print package redo require sub undef unless until use wantarray while BEGIN END ",hashComments:b,multiLineStrings:b,regexLiterals:b}),["perl","pl","pm"]);
U(S({keywords:"break continue do else for if return while alias and begin case class def defined elsif end ensure false in module next nil not or redo rescue retry self super then true undef unless until when yield BEGIN END ",hashComments:b,multiLineStrings:b,regexLiterals:b}),["rb"]);
U(S({keywords:"break continue do else for if return while auto case char const default double enum extern float goto int long register short signed sizeof static struct switch typedef union unsigned void volatile catch class delete false import new operator private protected public this throw true try typeof debugger eval export function get null set undefined var with Infinity NaN ",cStyleComments:b,regexLiterals:b}),["js"]);
U(S({keywords:"all and by catch class else extends false finally for if in is isnt loop new no not null of off on or return super then true try unless until when while yes ",hashComments:3,cStyleComments:b,multilineStrings:b,tripleQuotedStrings:b,regexLiterals:b}),["coffee"]);U(R([],[["str",/^[\s\S]+/]]),["regex"]);window.PR_normalizedHtml=M;window.prettyPrintOne=ta;window.prettyPrint=Aa;
window.PR={combinePrefixPatterns:N,createSimpleLexer:R,registerLangHandler:U,sourceDecorator:S,PR_ATTRIB_NAME:"atn",PR_ATTRIB_VALUE:"atv",PR_COMMENT:"com",PR_DECLARATION:"dec",PR_KEYWORD:"kwd",PR_LITERAL:"lit",PR_NOCODE:"nocode",PR_PLAIN:"pln",PR_PUNCTUATION:"pun",PR_SOURCE:"src",PR_STRING:"str",PR_TAG:"tag",PR_TYPE:"typ"};/*
 Copyright (C) 2009 Onno Hommes.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_COMMENT,/^#[^\r\n]*/,l,"#"],[PR.PR_PLAIN,/^[\t\n\r \xA0]+/,l,"\t\n\r \u00a0"],[PR.PR_STRING,/^\"(?:[^\"\\]|\\[\s\S])*(?:\"|$)/,l,'"']],[[PR.PR_KEYWORD,/^(?:ADS|AD|AUG|BZF|BZMF|CAE|CAF|CA|CCS|COM|CS|DAS|DCA|DCOM|DCS|DDOUBL|DIM|DOUBLE|DTCB|DTCF|DV|DXCH|EDRUPT|EXTEND|INCR|INDEX|NDX|INHINT|LXCH|MASK|MSK|MP|MSU|NOOP|OVSK|QXCH|RAND|READ|RELINT|RESUME|RETURN|ROR|RXOR|SQUARE|SU|TCR|TCAA|OVSK|TCF|TC|TS|WAND|WOR|WRITE|XCH|XLQ|XXALQ|ZL|ZQ|ADD|ADZ|SUB|SUZ|MPY|MPR|MPZ|DVP|COM|ABS|CLA|CLZ|LDQ|STO|STQ|ALS|LLS|LRS|TRA|TSQ|TMI|TOV|AXT|TIX|DLY|INP|OUT)\s/,
l],[PR.PR_TYPE,/^(?:-?GENADR|=MINUS|2BCADR|VN|BOF|MM|-?2CADR|-?[1-6]DNADR|ADRES|BBCON|[SE]?BANK\=?|BLOCK|BNKSUM|E?CADR|COUNT\*?|2?DEC\*?|-?DNCHAN|-?DNPTR|EQUALS|ERASE|MEMORY|2?OCT|REMADR|SETLOC|SUBRO|ORG|BSS|BES|SYN|EQU|DEFINE|END)\s/,l],[PR.PR_LITERAL,/^\'(?:-*(?:\w|\\[\x21-\x7e])(?:[\w-]*|\\[\x21-\x7e])[=!?]?)?/],[PR.PR_PLAIN,/^-*(?:[!-z_]|\\[\x21-\x7e])(?:[\w-]*|\\[\x21-\x7e])[=!?]?/i],[PR.PR_PUNCTUATION,/^[^\w\t\n\r \xA0()\"\\\';]+/]]),["apollo","agc","aea"]);/*
 Copyright (C) 2011 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.createSimpleLexer([["opn",/^[\(\{\[]+/,l,"([{"],["clo",/^[\)\}\]]+/,l,")]}"],[PR.PR_COMMENT,/^;[^\r\n]*/,l,";"],[PR.PR_PLAIN,/^[\t\n\r \xA0]+/,l,"\t\n\r \u00a0"],[PR.PR_STRING,/^\"(?:[^\"\\]|\\[\s\S])*(?:\"|$)/,l,'"']],[[PR.PR_KEYWORD,/^(?:def|if|do|let|quote|var|fn|loop|recur|throw|try|monitor-enter|monitor-exit|defmacro|defn|defn-|macroexpand|macroexpand-1|for|doseq|dosync|dotimes|and|or|when|not|assert|doto|proxy|defstruct|first|rest|cons|defprotocol|deftype|defrecord|reify|defmulti|defmethod|meta|with-meta|ns|in-ns|create-ns|import|intern|refer|alias|namespace|resolve|ref|deref|refset|new|set!|memfn|to-array|into-array|aset|gen-class|reduce|map|filter|find|nil?|empty?|hash-map|hash-set|vec|vector|seq|flatten|reverse|assoc|dissoc|list|list?|disj|get|union|difference|intersection|extend|extend-type|extend-protocol|prn)\b/,
l],[PR.PR_TYPE,/^:[0-9a-zA-Z\-]+/]]),["clj"]);/*
 Copyright (C) 2009 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_PLAIN,/^[ \t\r\n\f]+/,l," \t\r\n\f"]],[[PR.PR_STRING,/^\"(?:[^\n\r\f\\\"]|\\(?:\r\n?|\n|\f)|\\[\s\S])*\"/,l],[PR.PR_STRING,/^\'(?:[^\n\r\f\\\']|\\(?:\r\n?|\n|\f)|\\[\s\S])*\'/,l],["lang-css-str",/^url\(([^\)\"\']*)\)/i],[PR.PR_KEYWORD,/^(?:url|rgb|\!important|@import|@page|@media|@charset|inherit)(?=[^\-\w]|$)/i,l],["lang-css-kw",/^(-?(?:[_a-z]|(?:\\[0-9a-f]+ ?))(?:[_a-z0-9\-]|\\(?:\\[0-9a-f]+ ?))*)\s*:/i],[PR.PR_COMMENT,/^\/\*[^*]*\*+(?:[^\/*][^*]*\*+)*\//],
[PR.PR_COMMENT,/^(?:<\!--|--\>)/],[PR.PR_LITERAL,/^(?:\d+|\d*\.\d+)(?:%|[a-z]+)?/i],[PR.PR_LITERAL,/^#(?:[0-9a-f]{3}){1,2}/i],[PR.PR_PLAIN,/^-?(?:[_a-z]|(?:\\[\da-f]+ ?))(?:[_a-z\d\-]|\\(?:\\[\da-f]+ ?))*/i],[PR.PR_PUNCTUATION,/^[^\s\w\'\"]+/]]),["css"]);PR.registerLangHandler(PR.createSimpleLexer([],[[PR.PR_KEYWORD,/^-?(?:[_a-z]|(?:\\[\da-f]+ ?))(?:[_a-z\d\-]|\\(?:\\[\da-f]+ ?))*/i]]),["css-kw"]);PR.registerLangHandler(PR.createSimpleLexer([],[[PR.PR_STRING,/^[^\)\"\']+/]]),["css-str"]);/*
 Copyright (C) 2010 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_PLAIN,/^[\t\n\r \xA0]+/,l,"\t\n\r \u00a0"],[PR.PR_PLAIN,/^(?:\"(?:[^\"\\]|\\[\s\S])*(?:\"|$)|\'(?:[^\'\\]|\\[\s\S])+(?:\'|$))/,l,"\"'"]],[[PR.PR_COMMENT,/^(?:\/\/[^\r\n]*|\/\*[\s\S]*?\*\/)/],[PR.PR_PLAIN,/^(?:[^\/\"\']|\/(?![\/\*]))+/i]]),["go"]);/*
 Copyright (C) 2009 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_PLAIN,/^[\t\n\x0B\x0C\r ]+/,l,"\t\n\x0B\f\r "],[PR.PR_STRING,/^\"(?:[^\"\\\n\x0C\r]|\\[\s\S])*(?:\"|$)/,l,'"'],[PR.PR_STRING,/^\'(?:[^\'\\\n\x0C\r]|\\[^&])\'?/,l,"'"],[PR.PR_LITERAL,/^(?:0o[0-7]+|0x[\da-f]+|\d+(?:\.\d+)?(?:e[+\-]?\d+)?)/i,l,"0123456789"]],[[PR.PR_COMMENT,/^(?:(?:--+(?:[^\r\n\x0C]*)?)|(?:\{-(?:[^-]|-+[^-\}])*-\}))/],[PR.PR_KEYWORD,/^(?:case|class|data|default|deriving|do|else|if|import|in|infix|infixl|infixr|instance|let|module|newtype|of|then|type|where|_)(?=[^a-zA-Z0-9\']|$)/,
l],[PR.PR_PLAIN,/^(?:[A-Z][\w\']*\.)*[a-zA-Z][\w\']*/],[PR.PR_PUNCTUATION,/^[^\t\n\x0B\x0C\r a-zA-Z0-9\'\"]+/]]),["hs"]);/*
 Copyright (C) 2008 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.createSimpleLexer([["opn",/^\(+/,l,"("],["clo",/^\)+/,l,")"],[PR.PR_COMMENT,/^;[^\r\n]*/,l,";"],[PR.PR_PLAIN,/^[\t\n\r \xA0]+/,l,"\t\n\r \u00a0"],[PR.PR_STRING,/^\"(?:[^\"\\]|\\[\s\S])*(?:\"|$)/,l,'"']],[[PR.PR_KEYWORD,/^(?:block|c[ad]+r|catch|con[ds]|def(?:ine|un)|do|eq|eql|equal|equalp|eval-when|flet|format|go|if|labels|lambda|let|load-time-value|locally|macrolet|multiple-value-call|nil|progn|progv|quote|require|return-from|setq|symbol-macrolet|t|tagbody|the|throw|unwind)\b/,
l],[PR.PR_LITERAL,/^[+\-]?(?:[0#]x[0-9a-f]+|\d+\/\d+|(?:\.\d+|\d+(?:\.\d*)?)(?:[ed][+\-]?\d+)?)/i],[PR.PR_LITERAL,/^\'(?:-*(?:\w|\\[\x21-\x7e])(?:[\w-]*|\\[\x21-\x7e])[=!?]?)?/],[PR.PR_PLAIN,/^-*(?:[a-z_]|\\[\x21-\x7e])(?:[\w-]*|\\[\x21-\x7e])[=!?]?/i],[PR.PR_PUNCTUATION,/^[^\w\t\n\r \xA0()\"\\\';]+/]]),["cl","el","lisp","scm"]);/*
 Copyright (C) 2008 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_PLAIN,/^[\t\n\r \xA0]+/,l,"\t\n\r \u00a0"],[PR.PR_STRING,/^(?:\"(?:[^\"\\]|\\[\s\S])*(?:\"|$)|\'(?:[^\'\\]|\\[\s\S])*(?:\'|$))/,l,"\"'"]],[[PR.PR_COMMENT,/^--(?:\[(=*)\[[\s\S]*?(?:\]\1\]|$)|[^\r\n]*)/],[PR.PR_STRING,/^\[(=*)\[[\s\S]*?(?:\]\1\]|$)/],[PR.PR_KEYWORD,/^(?:and|break|do|else|elseif|end|false|for|function|if|in|local|nil|not|or|repeat|return|then|true|until|while)\b/,l],[PR.PR_LITERAL,/^[+-]?(?:0x[\da-f]+|(?:(?:\.\d+|\d+(?:\.\d*)?)(?:e[+\-]?\d+)?))/i],
[PR.PR_PLAIN,/^[a-z_]\w*/i],[PR.PR_PUNCTUATION,/^[^\w\t\n\r \xA0][^\w\t\n\r \xA0\"\'\-\+=]*/]]),["lua"]);/*
 Copyright (C) 2008 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_PLAIN,/^[\t\n\r \xA0]+/,l,"\t\n\r \u00a0"],[PR.PR_COMMENT,/^#(?:if[\t\n\r \xA0]+(?:[a-z_$][\w\']*|``[^\r\n\t`]*(?:``|$))|else|endif|light)/i,l,"#"],[PR.PR_STRING,/^(?:\"(?:[^\"\\]|\\[\s\S])*(?:\"|$)|\'(?:[^\'\\]|\\[\s\S])(?:\'|$))/,l,"\"'"]],[[PR.PR_COMMENT,/^(?:\/\/[^\r\n]*|\(\*[\s\S]*?\*\))/],[PR.PR_KEYWORD,/^(?:abstract|and|as|assert|begin|class|default|delegate|do|done|downcast|downto|elif|else|end|exception|extern|false|finally|for|fun|function|if|in|inherit|inline|interface|internal|lazy|let|match|member|module|mutable|namespace|new|null|of|open|or|override|private|public|rec|return|static|struct|then|to|true|try|type|upcast|use|val|void|when|while|with|yield|asr|land|lor|lsl|lsr|lxor|mod|sig|atomic|break|checked|component|const|constraint|constructor|continue|eager|event|external|fixed|functor|global|include|method|mixin|object|parallel|process|protected|pure|sealed|trait|virtual|volatile)\b/],
[PR.PR_LITERAL,/^[+\-]?(?:0x[\da-f]+|(?:(?:\.\d+|\d+(?:\.\d*)?)(?:e[+\-]?\d+)?))/i],[PR.PR_PLAIN,/^(?:[a-z_][\w']*[!?#]?|``[^\r\n\t`]*(?:``|$))/i],[PR.PR_PUNCTUATION,/^[^\t\n\r \xA0\"\'\w]+/]]),["fs","ml"]);/*
 Copyright (C) 2006 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.sourceDecorator({keywords:"bool bytes default double enum extend extensions false fixed32 fixed64 float group import int32 int64 max message option optional package repeated required returns rpc service sfixed32 sfixed64 sint32 sint64 string syntax to true uint32 uint64",cStyleComments:b}),["proto"]);/*
 Copyright (C) 2010 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_PLAIN,/^[\t\n\r \xA0]+/,l,"\t\n\r \u00a0"],[PR.PR_STRING,/^(?:"(?:(?:""(?:""?(?!")|[^\\"]|\\.)*"{0,3})|(?:[^"\r\n\\]|\\.)*"?))/,l,'"'],[PR.PR_LITERAL,/^`(?:[^\r\n\\`]|\\.)*`?/,l,"`"],[PR.PR_PUNCTUATION,/^[!#%&()*+,\-:;<=>?@\[\\\]^{|}~]+/,l,"!#%&()*+,-:;<=>?@[\\]^{|}~"]],[[PR.PR_STRING,/^'(?:[^\r\n\\']|\\(?:'|[^\r\n']+))'/],[PR.PR_LITERAL,/^'[a-zA-Z_$][\w$]*(?!['$\w])/],[PR.PR_KEYWORD,/^(?:abstract|case|catch|class|def|do|else|extends|final|finally|for|forSome|if|implicit|import|lazy|match|new|object|override|package|private|protected|requires|return|sealed|super|throw|trait|try|type|val|var|while|with|yield)\b/],
[PR.PR_LITERAL,/^(?:true|false|null|this)\b/],[PR.PR_LITERAL,/^(?:(?:0(?:[0-7]+|X[0-9A-F]+))L?|(?:(?:0|[1-9][0-9]*)(?:(?:\.[0-9]+)?(?:E[+\-]?[0-9]+)?F?|L?))|\\.[0-9]+(?:E[+\-]?[0-9]+)?F?)/i],[PR.PR_TYPE,/^[$_]*[A-Z][_$A-Z0-9]*[a-z][\w$]*/],[PR.PR_PLAIN,/^[$a-zA-Z_][\w$]*/],[PR.PR_COMMENT,/^\/(?:\/.*|\*(?:\/|\**[^*/])*(?:\*+\/?)?)/],[PR.PR_PUNCTUATION,/^(?:\.+|\/)/]]),["scala"]);/*
 Copyright (C) 2008 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_PLAIN,/^[\t\n\r \xA0]+/,l,"\t\n\r \u00a0"],[PR.PR_STRING,/^(?:"(?:[^\"\\]|\\.)*"|'(?:[^\'\\]|\\.)*')/,l,"\"'"]],[[PR.PR_COMMENT,/^(?:--[^\r\n]*|\/\*[\s\S]*?(?:\*\/|$))/],[PR.PR_KEYWORD,/^(?:ADD|ALL|ALTER|AND|ANY|AS|ASC|AUTHORIZATION|BACKUP|BEGIN|BETWEEN|BREAK|BROWSE|BULK|BY|CASCADE|CASE|CHECK|CHECKPOINT|CLOSE|CLUSTERED|COALESCE|COLLATE|COLUMN|COMMIT|COMPUTE|CONSTRAINT|CONTAINS|CONTAINSTABLE|CONTINUE|CONVERT|CREATE|CROSS|CURRENT|CURRENT_DATE|CURRENT_TIME|CURRENT_TIMESTAMP|CURRENT_USER|CURSOR|DATABASE|DBCC|DEALLOCATE|DECLARE|DEFAULT|DELETE|DENY|DESC|DISK|DISTINCT|DISTRIBUTED|DOUBLE|DROP|DUMMY|DUMP|ELSE|END|ERRLVL|ESCAPE|EXCEPT|EXEC|EXECUTE|EXISTS|EXIT|FETCH|FILE|FILLFACTOR|FOR|FOREIGN|FREETEXT|FREETEXTTABLE|FROM|FULL|FUNCTION|GOTO|GRANT|GROUP|HAVING|HOLDLOCK|IDENTITY|IDENTITYCOL|IDENTITY_INSERT|IF|IN|INDEX|INNER|INSERT|INTERSECT|INTO|IS|JOIN|KEY|KILL|LEFT|LIKE|LINENO|LOAD|NATIONAL|NOCHECK|NONCLUSTERED|NOT|NULL|NULLIF|OF|OFF|OFFSETS|ON|OPEN|OPENDATASOURCE|OPENQUERY|OPENROWSET|OPENXML|OPTION|OR|ORDER|OUTER|OVER|PERCENT|PLAN|PRECISION|PRIMARY|PRINT|PROC|PROCEDURE|PUBLIC|RAISERROR|READ|READTEXT|RECONFIGURE|REFERENCES|REPLICATION|RESTORE|RESTRICT|RETURN|REVOKE|RIGHT|ROLLBACK|ROWCOUNT|ROWGUIDCOL|RULE|SAVE|SCHEMA|SELECT|SESSION_USER|SET|SETUSER|SHUTDOWN|SOME|STATISTICS|SYSTEM_USER|TABLE|TEXTSIZE|THEN|TO|TOP|TRAN|TRANSACTION|TRIGGER|TRUNCATE|TSEQUAL|UNION|UNIQUE|UPDATE|UPDATETEXT|USE|USER|VALUES|VARYING|VIEW|WAITFOR|WHEN|WHERE|WHILE|WITH|WRITETEXT)(?=[^\w-]|$)/i,
l],[PR.PR_LITERAL,/^[+-]?(?:0x[\da-f]+|(?:(?:\.\d+|\d+(?:\.\d*)?)(?:e[+\-]?\d+)?))/i],[PR.PR_PLAIN,/^[a-z_][\w-]*/i],[PR.PR_PUNCTUATION,/^[^\w\t\n\r \xA0\"\'][^\w\t\n\r \xA0+\-\"\']*/]]),["sql"]);/*
 Copyright (C) 2009 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_PLAIN,/^[\t\n\r \xA0\u2028\u2029]+/,l,"\t\n\r \u00a0\u2028\u2029"],[PR.PR_STRING,/^(?:[\"\u201C\u201D](?:[^\"\u201C\u201D]|[\"\u201C\u201D]{2})(?:[\"\u201C\u201D]c|$)|[\"\u201C\u201D](?:[^\"\u201C\u201D]|[\"\u201C\u201D]{2})*(?:[\"\u201C\u201D]|$))/i,l,'"\u201c\u201d'],[PR.PR_COMMENT,/^[\'\u2018\u2019][^\r\n\u2028\u2029]*/,l,"'\u2018\u2019"]],[[PR.PR_KEYWORD,/^(?:AddHandler|AddressOf|Alias|And|AndAlso|Ansi|As|Assembly|Auto|Boolean|ByRef|Byte|ByVal|Call|Case|Catch|CBool|CByte|CChar|CDate|CDbl|CDec|Char|CInt|Class|CLng|CObj|Const|CShort|CSng|CStr|CType|Date|Decimal|Declare|Default|Delegate|Dim|DirectCast|Do|Double|Each|Else|ElseIf|End|EndIf|Enum|Erase|Error|Event|Exit|Finally|For|Friend|Function|Get|GetType|GoSub|GoTo|Handles|If|Implements|Imports|In|Inherits|Integer|Interface|Is|Let|Lib|Like|Long|Loop|Me|Mod|Module|MustInherit|MustOverride|MyBase|MyClass|Namespace|New|Next|Not|NotInheritable|NotOverridable|Object|On|Option|Optional|Or|OrElse|Overloads|Overridable|Overrides|ParamArray|Preserve|Private|Property|Protected|Public|RaiseEvent|ReadOnly|ReDim|RemoveHandler|Resume|Return|Select|Set|Shadows|Shared|Short|Single|Static|Step|Stop|String|Structure|Sub|SyncLock|Then|Throw|To|Try|TypeOf|Unicode|Until|Variant|Wend|When|While|With|WithEvents|WriteOnly|Xor|EndIf|GoSub|Let|Variant|Wend)\b/i,
l],[PR.PR_COMMENT,/^REM[^\r\n\u2028\u2029]*/i],[PR.PR_LITERAL,/^(?:True\b|False\b|Nothing\b|\d+(?:E[+\-]?\d+[FRD]?|[FRDSIL])?|(?:&H[0-9A-F]+|&O[0-7]+)[SIL]?|\d*\.\d+(?:E[+\-]?\d+)?[FRD]?|#\s+(?:\d+[\-\/]\d+[\-\/]\d+(?:\s+\d+:\d+(?::\d+)?(\s*(?:AM|PM))?)?|\d+:\d+(?::\d+)?(\s*(?:AM|PM))?)\s+#)/i],[PR.PR_PLAIN,/^(?:(?:[a-z]|_\w)\w*|\[(?:[a-z]|_\w)\w*\])/i],[PR.PR_PUNCTUATION,/^[^\w\t\n\r \"\'\[\]\xA0\u2018\u2019\u201C\u201D\u2028\u2029]+/],[PR.PR_PUNCTUATION,/^(?:\[|\])/]]),["vb","vbs"]);PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_PLAIN,/^[\t\n\r \xA0]+/,l,"\t\n\r \u00a0"]],[[PR.PR_STRING,/^(?:[BOX]?"(?:[^\"]|"")*"|'.')/i],[PR.PR_COMMENT,/^--[^\r\n]*/],[PR.PR_KEYWORD,/^(?:abs|access|after|alias|all|and|architecture|array|assert|attribute|begin|block|body|buffer|bus|case|component|configuration|constant|disconnect|downto|else|elsif|end|entity|exit|file|for|function|generate|generic|group|guarded|if|impure|in|inertial|inout|is|label|library|linkage|literal|loop|map|mod|nand|new|next|nor|not|null|of|on|open|or|others|out|package|port|postponed|procedure|process|pure|range|record|register|reject|rem|report|return|rol|ror|select|severity|shared|signal|sla|sll|sra|srl|subtype|then|to|transport|type|unaffected|units|until|use|variable|wait|when|while|with|xnor|xor)(?=[^\w-]|$)/i,
l],[PR.PR_TYPE,/^(?:bit|bit_vector|character|boolean|integer|real|time|string|severity_level|positive|natural|signed|unsigned|line|text|std_u?logic(?:_vector)?)(?=[^\w-]|$)/i,l],[PR.PR_TYPE,/^\'(?:ACTIVE|ASCENDING|BASE|DELAYED|DRIVING|DRIVING_VALUE|EVENT|HIGH|IMAGE|INSTANCE_NAME|LAST_ACTIVE|LAST_EVENT|LAST_VALUE|LEFT|LEFTOF|LENGTH|LOW|PATH_NAME|POS|PRED|QUIET|RANGE|REVERSE_RANGE|RIGHT|RIGHTOF|SIMPLE_NAME|STABLE|SUCC|TRANSACTION|VAL|VALUE)(?=[^\w-]|$)/i,l],[PR.PR_LITERAL,/^\d+(?:_\d+)*(?:#[\w\\.]+#(?:[+\-]?\d+(?:_\d+)*)?|(?:\.\d+(?:_\d+)*)?(?:E[+\-]?\d+(?:_\d+)*)?)/i],
[PR.PR_PLAIN,/^(?:[a-z]\w*|\\[^\\]*\\)/i],[PR.PR_PUNCTUATION,/^[^\w\t\n\r \xA0\"\'][^\w\t\n\r \xA0\-\"\']*/]]),["vhdl","vhd"]);/*
 Copyright (C) 2009 Google Inc.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_PLAIN,/^[\t \xA0a-gi-z0-9]+/,l,"\t \u00a0abcdefgijklmnopqrstuvwxyz0123456789"],[PR.PR_PUNCTUATION,/^[=*~\^\[\]]+/,l,"=*~^[]"]],[["lang-wiki.meta",/(?:^^|\r\n?|\n)(#[a-z]+)\b/],[PR.PR_LITERAL,/^(?:[A-Z][a-z][a-z0-9]+[A-Z][a-z][a-zA-Z0-9]+)\b/],["lang-",/^\{\{\{([\s\S]+?)\}\}\}/],["lang-",/^`([^\r\n`]+)`/],[PR.PR_STRING,/^https?:\/\/[^\/?#\s]*(?:\/[^?#\s]*)?(?:\?[^#\s]*)?(?:#\S*)?/i],[PR.PR_PLAIN,/^(?:\r\n|[\s\S])[^#=*~^A-Zh\{`\[\r\n]*/]]),["wiki"]);
PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_KEYWORD,/^#[a-z]+/i,l,"#"]],[]),["wiki.meta"]);PR.registerLangHandler(PR.createSimpleLexer([[PR.PR_PUNCTUATION,/^[:|>?]+/,l,":|>?"],[PR.PR_DECLARATION,/^%(?:YAML|TAG)[^#\r\n]+/,l,"%"],[PR.PR_TYPE,/^[&]\S+/,l,"&"],[PR.PR_TYPE,/^!\S*/,l,"!"],[PR.PR_STRING,/^"(?:[^\\"]|\\.)*(?:"|$)/,l,'"'],[PR.PR_STRING,/^'(?:[^']|'')*(?:'|$)/,l,"'"],[PR.PR_COMMENT,/^#[^\r\n]*/,l,"#"],[PR.PR_PLAIN,/^\s+/,l," \t\r\n"]],[[PR.PR_DECLARATION,/^(?:---|\.\.\.)(?:[\r\n]|$)/],[PR.PR_PUNCTUATION,/^-/],[PR.PR_KEYWORD,/^\w+:[ \r\n]/],[PR.PR_PLAIN,/^\w+/]]),["yaml","yml"]);
