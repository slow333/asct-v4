from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag
def build_sort_url(sort_field, current_sort, current_order, search_title=None):
    """
    정렬 URL을 생성하는 템플릿 태그
    Args:
        sort_field: 정렬할 필드명 (예: 'title', 'unit_price')
        current_sort: 현재 정렬 필드
        current_order: 현재 정렬 순서 ('asc' or 'desc')
        search_title: 검색 제목 (선택사항)
    Returns:
        쿼리 문자열 (예: '?sort=title&order=desc&search_title=...')
    """
    params = {'sort': sort_field}
    
    # 같은 필드로 정렬하면 순서 토글, 다른 필드면 asc로 시작
    if sort_field == current_sort and current_order == 'asc':
        params['order'] = 'desc'
    else:
        params['order'] = 'asc'
    
    # 검색어가 있으면 추가
    if search_title:
        params['search_title'] = search_title
    
    return '?' + urlencode(params)


@register.simple_tag
def build_page_url(page_num, search_title=None, sort=None, order=None):
    """
    페이지 URL을 생성하는 템플릿 태그
    Args:
        page_num: 페이지 번호
        search_title: 검색 제목 (선택사항)
        sort: 정렬 필드 (선택사항)
        order: 정렬 순서 (선택사항)
    Returns:
        쿼리 문자열 (예: '?page=2&search_title=...&sort=title&order=asc')
    """
    params = {'page': page_num}
    
    if search_title:
        params['search_title'] = search_title
    if sort:
        params['sort'] = sort
    if order:
        params['order'] = order
    
    return '?' + urlencode(params)

@register.filter
def is_current_sort(sort_field, current_sort):
    """
    현재 정렬 필드인지 확인하는 필터
    Args:
        sort_field: 확인할 필드명
        current_sort: 현재 정렬 필드
    Returns:
        True/False
    """
    return sort_field == current_sort
