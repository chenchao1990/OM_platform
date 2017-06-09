#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.utils.safestring import mark_safe
from time import sleep


class PageInfo(object):
                        # 当前页       搜索到的数据的个数
    def __init__(self, currentPage, totalItems, perItems=20, pageNum=11):
        try:
            currentPage = int(currentPage)      # 页数
        except Exception, e:
            currentPage = 1

        self.__currentPage = currentPage                # 当前页
        self.__perItems = perItems                      # 每一页默认个数据个数
        self.__totalItems = totalItems                  # 搜素到的数据
        self.__pageNum = pageNum                        # 显示的页面个数

    @property
    def current_page(self):
        return self.__currentPage

    @property
    def total_items(self):
        return self.__totalItems

    @property
    def total_page(self):
        if not self.__totalItems:
            self.__totalItems = 0       # 计算余数是否大于0
        val = self.__totalItems/self.__perItems + 1 if self.__totalItems % self.__perItems > 0 else self.__totalItems/self.__perItems
        return val

    @property
    def page_num(self):
        return self.__pageNum

    @property
    def start(self):                        # 当前页面 数据开始的位置
        val = (self.__currentPage - 1) * self.__perItems
        return val

    @property
    def end(self):                          # 数据结束的位置
        val = self.__currentPage * self.__perItems
        return val

    def pager(self, baseurl=None):       # 首页中的分页
        '''
        page:当前页
        all_page_count: 需要显示的总页数
        '''
        page_html = []
        page = self.current_page
        all_page_count = self.total_page
        total_items = self.total_items

        # 首页
        # first_html = "<li><a class='button next' href='javascript:void(0)' onclick='ChangePage(1)'>首页</a></li>"
        first_html = "<li><a class='button previous' href='javascript:void(0)' onclick='ChangePage(1)'>首页</a></li>"
        page_html.append(first_html)

        # 上一页
        if page <= 1:
            # prev_html = "<li  class='disabled'><a class='button next' href='javascript:void(0)'>上一页</a></li>"
            prev_html = "<li><a class='button previous disabled' href='javascript:void(0)'>上一页</a></li>"
        else:
            # prev_html = "<li><a class='button next' href='javascript:void(0)' onclick='ChangePage(%d)'>上一页</a></li>" % (page-1, )
            prev_html = "<li><a class='button previous' href='javascript:void(0)' onclick='ChangePage(%d)'>上一页</a></li>" % (page-1, )
        page_html.append(prev_html)

        # 11个页码
        if all_page_count < 11:
            begin = 0
            end = all_page_count

        # 总页数大于 11
        else:
            #
            if page < 6:
                begin = 0
                end = 11
            else:
                if page + 6 > all_page_count:
                    begin = page - 6
                    end = all_page_count
                else:
                    begin = page - 6
                    end = page + 5

        for i in range(begin, end):
            # 当前页

            if page == i+1:
                # a_html = "<li class='active'><a class='button previous' href='javascript:void(0)' onclick='ChangePage(%d)'>%d</a></li>" % (i+1, i+1, )
                page_num = "<li><a class='active' href='javascript:void(0)' onclick='ChangePage(%d)'>%d</a></li>" % (i+1, i+1, )
                page_html.append(page_num)
            else:
                page_num = "<li><a href='javascript:void(0)' onclick='ChangePage(%d)'>%d</a></li>" % (i+1, i+1, )
                page_html.append(page_num)

        # 下一页
        if page+1 > all_page_count:
            # next_html = "<li class='disabled'><a class='button next ' href='javascript:void(0)'>下一页</a></li>"
            next_html = "<li><a class='button next disabled' href='javascript:void(0)'>下一页</a></li>"
        else:
            next_html = "<li><a class='button next' href='javascript:void(0)' onclick='ChangePage(%d)' >下一页</a><li>" % (page+1, )

        page_html.append(next_html)
        # 尾页
        end_html = "<li><a class='button next' href='javascript:void(0)' onclick='ChangePage(%d)'>尾页</a></li>" % (all_page_count, )
        page_html.append(end_html)

        # 页码概要
        end_html = "<li><a class='button next'  href='javascript:void(0)' >共 %d页 / %d 条数据</a></li>" % (all_page_count,total_items, )
        page_html.append(end_html)

        # 将列表中的元素拼接成页码字符串
        page_string = mark_safe(''.join(page_html))

        return page_string