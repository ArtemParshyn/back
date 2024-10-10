var thirstyFunctions;jQuery(document).ready(function($){thirstyFunctions={recordLinkStatEvents:function(){if(thirsty_global_vars.enable_record_stats=='yes')
$('body').on('click','a',thirstyFunctions.recordLinkStat);},recordLinkStat:function(e){var $link=$(this),href=$link.attr('href'),linkID=$link.data('linkid'),keyword=$link[0].innerText,qs=href?href.split('?')[1]:'',imgsrc,newWindow;if(!keyword)keyword=$link.text();if(!thirstyFunctions.isThirstyLink(href)&&!linkID)return;if($link.data("clicked")){e.preventDefault();return;}
$link.data("clicked",true);if(!keyword&&$link.find('img').length){imgsrc=$link.find('img').prop('src').split('/');keyword=imgsrc[imgsrc.length-1];}
if(thirsty_global_vars.enable_js_redirect==='yes'&&$link.data('nojs')!=true){e.preventDefault();if($link.prop('target')=='_blank'&&!thirstyFunctions.disableNewWindow())
newWindow=window.open('','_blank');}
$.post(thirsty_global_vars.ajax_url,{action:'ta_click_data_redirect',href:href,page:window.location.href,link_id:linkID,keyword:keyword,qs:qs},function(redirect_url){$link.data("clicked",false);if(thirsty_global_vars.enable_js_redirect!=='yes'||$link.data('nojs')==true)
return;if(newWindow)
newWindow.location.href=redirect_url?redirect_url:href;else
window.location.href=redirect_url?redirect_url:href;}).fail(function(){$link.data("clicked",false);if(thirsty_global_vars.enable_js_redirect!=='yes'||$link.data('nojs')==true)
return;if(newWindow)
newWindow.location.href=href;else
window.location.href=href;});},disableNewWindow:function(){var strings=['FBAN','MessengerForiOS','FBAV','Instagram','Pinterest','Twitter','Electron','Steam'];for(var x in strings){if(navigator.userAgent.indexOf(strings[x])>=0)
return true;}
return false;},isThirstyLink:function(href){if(!href)
return;href=href.replace('http:','{protocol}').replace('https:','{protocol}');var link_uri=href.replace(thirsty_global_vars.home_url,'').replace('{protocol}',''),link_prefix,new_href;link_uri=link_uri.indexOf('/')==0?link_uri.replace('/',''):link_uri;link_prefix=link_uri.substr(0,link_uri.indexOf('/')),new_href=href.replace('/'+link_prefix+'/','/'+thirsty_global_vars.link_prefix+'/').replace('{protocol}',window.location.protocol);return(link_prefix&&$.inArray(link_prefix,link_prefixes)>-1)?new_href:false;},linkFixer:function(){if(thirsty_global_vars.link_fixer_enabled!=='yes')
return;var $allLinks=$('body a'),hrefs=[],href,linkClass,isShortcode,isImage,key;for(key=0;key<$allLinks.length;key++){href=$($allLinks[key]).attr('href');linkClass=$($allLinks[key]).attr('class');isShortcode=$($allLinks[key]).data('shortcode');isImage=$($allLinks[key]).has('img').length;href=thirstyFunctions.isThirstyLink(href);if(href&&!isShortcode)
hrefs.push({key:key,class:linkClass,href:href,is_image:isImage});$($allLinks[key]).removeAttr('data-shortcode');}
if(hrefs.length<1)
return;$.post(thirsty_global_vars.ajax_url,{action:'ta_link_fixer',hrefs:hrefs,post_id:thirsty_global_vars.post_id},function(response){if(response.status=='success'){for(var x in response.data){if(typeof response.data[x]!='object')continue;var key=response.data[x]['key'],hrefProp=$($allLinks[key]).prop('href'),qs=hrefProp?hrefProp.split('?')[1]:'',href=response.data[x]['href'],title=response.data[x]['title'],className=response.data[x]['class'],connector;if(qs&&response.data[x]['pass_qs']){connector=href.indexOf('?')<0?'?':'&';href=href+connector+qs;}
href=href.replace('http:',window.location.protocol).replace('https:',window.location.protocol);if(title)
$($allLinks[key]).prop('title',title);else
$($allLinks[key]).removeAttr('title');if(thirsty_global_vars.disable_thirstylink_class=='yes')
className=className.replace('thirstylinkimg','').replace('thirstylink','').trim();if(className)
$($allLinks[key]).prop('class',className);else
$($allLinks[key]).removeAttr('class');$($allLinks[key]).prop('href',href).prop('rel',response.data[x]['rel']).prop('target',response.data[x]['target']).attr('data-linkid',response.data[x]['link_id']);if(thirsty_global_vars.enable_js_redirect==='yes')
$($allLinks[key]).attr('data-nojs',response.data[x]['nojs']);}}},'json');}}
var link_prefixes=$.map(thirsty_global_vars.link_prefixes,function(value,index){return[value];});thirstyFunctions.recordLinkStatEvents();thirstyFunctions.linkFixer();});