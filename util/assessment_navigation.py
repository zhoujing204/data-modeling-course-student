"""Safe, optional notebook navigation after a successful report receipt."""
from html import escape
import json
import re
from urllib.parse import urljoin, urlsplit, parse_qs


def open_assessment_after_upload(response, *, trusted_origin, display_html, open_browser, remote_kernel=False):
    result={'opened':False,'fallback_url':None,'assessment_available':False}
    if response.status_code not in (200,201):return result
    try:
        data=response.json(); raw=data.get('assessment_url','')
        base=urlsplit(trusted_origin); url=urlsplit(urljoin(trusted_origin,raw))
        query=parse_qs(url.query,keep_blank_values=True)
        if (base.scheme not in ('http','https') or (url.scheme,url.netloc)!=(base.scheme,base.netloc)
            or url.username or url.password or '\\' in raw or url.fragment or url.path!='/quiz'
            or set(query)!={'course_run_id','experiment_id'} or any(len(v)!=1 or not re.fullmatch(r'[A-Za-z0-9_-]+',v[0]) for v in query.values())):
            return result
        target=url.geturl()
        result.update(fallback_url=target,assessment_available=bool(data.get('assessment_available')))
        display_html('<p><a href="'+escape(target,quote=True)+'" target="_blank" rel="noopener">Open online assessment</a></p>')
        if remote_kernel and result['assessment_available']:
            display_html('<script>window.open('+json.dumps(target).replace('<','\\u003c')+',"_blank","noopener");</script>')
        elif result['assessment_available']:
            try:result['opened']=bool(open_browser(target))
            except OSError:pass
    except (ValueError,TypeError,AttributeError):pass
    return result
