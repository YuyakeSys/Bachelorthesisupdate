# Pagination component

from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, queryset, page_size=6, page_param='page', plus=4):

        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param
        page = request.GET.get(page_param, "1")

        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中的数据比较少，都没有达到11页。
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据库中的数据比较多 > 11页。

            # 当前页<5时（小极值）
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页 > 5
                # 当前页+5 > 总页面
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

            # 页码
        page_str_list = []

        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page-1])
            prev = '<li class="page-item"><a class="page-link" href="?{}"  aria-label="Previous"><span ' \
                   'aria-hidden="true">&laquo;</span></a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li class="page-item"><a class="page-link" href="?{}"  aria-label="Previous"><span ' \
                   'aria-hidden="true">&laquo;</span></a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                pagi = '<li class="page-item active"><a class="page-link" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                pagi = '<li class="page-item"><a class="page-link" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(pagi)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next_page = '<li class="page-item"><a class="page-link" href="?{}" aria-label="Next"><span ' \
                        'aria-hidden="true">&raquo;</span></a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            next_page = '<li class="page-item"><a class="page-link" href="?{}" aria-label="Next"><span ' \
                        'aria-hidden="true">&raquo;</span></a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(next_page)

        search_string = """<li><form style = "float: left; margin-left: -1px"method = "get" > <input name = "page" 
        style = "position: relative;float: left;display: inline - block;width: 80px;border - radius: 0;"type = 
        "text"class ="form-control me-1>placeholder="page" ><button class ="btn btn-outline-success" 
        type="submit">jump to</button></form></li> """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
