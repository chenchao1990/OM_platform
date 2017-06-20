
(function(jq){

    /*
    Asc排序
    end:数组长度
    args:要排序的数组，例：[{'key':11,'value':'Usa'},{'key':21,'value':'China']
     */
    function SortAsc(end,args){
        if(end<=0){
            return args;
        }else if(end == 1){
            return args;
        }else{
            var bigerIndex = end - 1;
            for(i = 0;i<end - 1;i++){
                if(args[i].value > args[bigerIndex].value){
                    bigerIndex = i;
                }
            }
            var temp = args[bigerIndex];
            args[bigerIndex] = args[end-1];
            args[end-1] = temp;
            return SortAsc(end-1,args);
        }
    }

    /*
    Desc排序
    end:数组中字典元素的个数
    args:要排序的数组，例：[{'key':11,'value':'Usa'},{'key':21,'value':'China']
     */
    function SortDesc(end,args){
        if(end<=0){                 // 当列表中元素个数小于等于0时，说明没有数据
            return args;
        }else if(end == 1){         //  当元素个数为1时，一条数据 不需要排序 直接返回
            return args;
        }else{                      // 大于1时 需要排序
            var smallerIndex = end - 1;
            for(i = 0;i<end - 1;i++){           //  循环 0 到 end的范围
                if(args[i].value < args[smallerIndex].value){

                    smallerIndex = i;
                }
            }
            var temp = args[smallerIndex];
            args[smallerIndex] = args[end-1];
            args[end-1] = temp;
            return SortDesc(end-1,args);
        }
    }
    //
    function DoTrIntoEdit($tr, specialInEditFunc){
        // tr 为被选中的那行数据
        $tr.find('td[edit-enable="true"]').each(function(){     // 找到tr下面所有td[edit-enable="true"] 并循环
            console.log("3333333333333333333333");
            ExecuteTdIntoEdit($(this), specialInEditFunc);

        });
    }

    function DoTrOutEdit($tr, specialOutEditFunc){
        $tr.find('td[edit-enable="true"]').each(function(){
            ExecuteTdOutEdit($(this), specialOutEditFunc);
        });
    }
    //进入编辑模式
    function ExecuteTdIntoEdit($td, specialInEditFunc){         // $td 为循环到的一条资产下某个td
        var editType = $td.attr('edit-type');
        //var editOption = $td.attr('edit-option');
        //var options = $td.attr('options');
        //var value_key = $td.attr('value_key');
        //var text_key = $td.attr('text_key');        // 获取各种能编辑的属性的值

        if(editType=='input'){                      // 判断editType为input时
            console.log("4444444444444444444");
            var text = $td.text();                  // 获取标签的文本
            $td.addClass('padding-3');              // 添加一个样式
            var htmlTag = $.CreateInput({'value':text,'class':'padding-tb-5 form-control '},
                                        {'width':'100%'});          // 返回的是一个input标签 已经设置了字典中的样式和属性
            $td.empty().append(htmlTag);            // 将这个td子元素清空 然后将新的input添加到里面

        }else if(editType=='select'){               // 当 == select时
            if(specialInEditFunc){                  // 判断specialInEditFunc 是否存在
                specialInEditFunc($td, editOption);
            }else{
                var text = $td.text();              // 获取这条资产下某个td的文本
                $td.addClass('padding-3');          // 添加一个样式
                var htmlTag = $.CreateSelect({'class':'padding-tb-5 form-control','onchange':'MultiSelect(this)'},
                                             {'width':'100%'},
                                             window[options],       //  window[options] 为所有带option属性的标签
                                             text,
                                            value_key,
                                            text_key);     // text为标签的文本
                // htmlTag 返回的是一个select标签 里面装有option标签
                $td.empty().append(htmlTag);        // 将td清空 在把心的select标签添加到td里面
            }
        }

    }

    function ExecuteTdOutEdit($td, specialOutEditFunc){
        var editType = $td.attr('edit-type');
        var editOption = $td.attr('edit-option');

        if(editType=='input'){
            var text = $td.children().first().val();
            $td.removeClass('padding-3');
            $td.empty().text(text);
        }else if(editType=='select'){

            if(specialOutEditFunc){
                specialOutEditFunc($td, editOption);
            }
            else{
                $td.removeClass('padding-3');
                var selecting_val = $td.children().first().val();           // 获取文本框中的值
                var selecting_text = $td.children().first().find("option[value='"+selecting_val+"']").text();
                $td.empty().append(selecting_text);
                $td.attr('new-value',selecting_val);
            }
        }
    }

	jq.extend({
        //将左侧菜单栏展开或收缩
        // 向正在点击的标签添加激活样式 然后将其他的标签删除激活样式
        'InitMenu':function(target, checked){
            $(target).addClass('open').siblings().each(function(){
                $(this).removeClass('open');
            });
            $(checked).addClass('selected-menu').parent().siblings().each(function () {
                $(this).children().first().removeClass('selected-menu')

            })
        },
        //创建一个div标签
        'CreateDiv':function(attrs,csses,text){
            var obj= document.createElement('div');      // 创建一个td的标签
            $.each(attrs,function(k,v){                 // 循环 属性的attrs
                $(obj).attr(k,v);
            });
            $.each(csses,function(k,v){                 // 循环 css的csses
                $(obj).css(k,v);
            });
            //为创建的td标签 添加html代码
            $(obj).html(text);
            return obj;
        },
        'CreateBigDiv':function(attrs,csses,div_list){
            var obj= document.createElement('div');      // 创建一个td的标签
            $.each(attrs,function(k,v){                 // 循环 属性的attrs
                $(obj).attr(k,v);
            });
            $.each(csses,function(k,v){                 // 循环 css的csses
                $(obj).css(k,v);
            });
            //为创建的td标签 添加html代码
            $.each(div_list,function(k,v){                   // 循环前面已经装有标签数据的列表 、
                $(v).appendTo($(obj));                  // 把$()中的元素追加到后面的$(obj)中  将列表中的标签追加到创建的tr中
            });
            return obj;
        },
        //text ：一个input标签 为checkbox
        'CreateTh':function(attrs,csses,text){
            var obj= document.createElement('th');      // 创建一个td的标签
            $.each(attrs,function(k,v){                 // 循环 属性的attrs
                $(obj).attr(k,v);
            });
            $.each(csses,function(k,v){                 // 循环 css的csses
                $(obj).css(k,v);
            });
            //为创建的td标签 添加html代码

            $(obj).html(text);
            return obj;
        },
        //text ：一个input标签 为checkbox
        'CreateTd':function(attrs,csses,text){
            var obj= document.createElement('td');      // 创建一个td的标签
            $.each(attrs,function(k,v){                 // 循环 属性的attrs
                $(obj).attr(k,v);
            });
            $.each(csses,function(k,v){                 // 循环 css的csses
                $(obj).css(k,v);
            });
            //为创建的td标签 添加html代码

            $(obj).html(text);
            return obj;
        },
        'CreateTds':function(attrs,csses,list,seprate){
            var obj= document.createElement('td');
            $.each(attrs,function(k,v){
                $(obj).attr(k,v);
            });
            $.each(csses,function(k,v){
                $(obj).css(k,v);
            });
            $.each(list,function(k,v){
                if(k == 0){
                    $(obj).append(v);
                }else{
                    $(obj).append(seprate);
                    $(obj).append(v);
                }
            });
            return obj;
        },
        'CreateTr':function(attrs,csses,tds){
            var obj= document.createElement('tr');      // 创建一个tr标签
            $.each(attrs,function(k,v){                 // 循环属性并添加
                $(obj).attr(k,v);
            });
            $.each(csses,function(k,v){
                $(obj).css(k,v);
            });
            $.each(tds,function(k,v){                   // 循环前面已经装有标签数据的列表 、
                $(v).appendTo($(obj));                  // 把$()中的元素追加到后面的$(obj)中  将列表中的标签追加到创建的tr中
            });
            return obj;                             // 返回一个tr
        },
        //attrs = {'type':'checkbox'}
        'CreateInput':function(attrs,csses){
            //创建一个input标签
            var obj= document.createElement('input');       // 创建一个input标签
            $.each(attrs,function(k,v){                     // 传过来的属性字典
                //为创建的input标签设置属性
                $(obj).attr(k,v);                           // 根据字典的key value 来设置创建input标签的属性
            });
            $.each(csses,function(k,v){                     // 根绝字典中的k  v  来设置input的样式
                //添加样式
                $(obj).css(k,v);
            });
            return obj;                                      // 将创建的Input标签返回
        },
        'CreateA':function(attrs,csses,text){
            var obj= document.createElement('a');       // 创建一个A标签
            $.each(attrs,function(k,v){                 // {href     id     target}
                $(obj).attr(k,v);                       // 为创建的A标签 添加属性
            });
            $.each(csses,function(k,v){
                $(obj).css(k,v);
            });
            $(obj).html(text);                          // 设置A标签的内容
            return obj
        },
        'CreateI':function(attrs,csses,text){
            var obj= document.createElement('i');       // 创建一个i标签
            $.each(attrs,function(k,v){                 // {href     id     target}
                $(obj).attr(k,v);                       // 为创建的i标签 添加属性
            });
            $.each(csses,function(k,v){
                $(obj).css(k,v);
            });
            $(obj).html(text);                          // 设置i标签的内容
            return obj
        },

        'CreateP':function(attrs,csses,text){
            var obj= document.createElement('p');       // 创建一个i标签
            $.each(attrs,function(k,v){                 // {href     id     target}
                $(obj).attr(k,v);                       // 为创建的i标签 添加属性
            });
            $.each(csses,function(k,v){
                $(obj).css(k,v);
            });
            $(obj).html(text);                          // 设置p标签的内容
            return obj
        },
        'CreateSpan':function(attrs,csses,text){
            var obj= document.createElement('span');       // 创建一个span标签
            $.each(attrs,function(k,v){                 // {href     id     target}
                $(obj).attr(k,v);                       // 为创建的i标签 添加属性
            });
            $.each(csses,function(k,v){
                $(obj).css(k,v);
            });
            $(obj).html(text);                          // 设置p标签的内容
            return obj
        },

        'GetCurrentActive':function(li_obj){
            var active_obj = $(li_obj).find("li[class='active']");
            return $(active_obj).children().first().attr('href');
        },

        /*
        创建Select标签
        options: 必须是含有id和name的对象，id作为option的value，name作为option的内容，例：obj.id = 1,obj.name = 'China'
        current: 当前被选中的内容，例：current ＝ 'China'
        key_value,key_text是全局字典的key和value的key    key_value为id  key_text为name
         */
        'CreateSelect': function(attrs,csses,options,current,key_value,key_text){
            var sel= document.createElement('select');          // 创建一个select标签
            $.each(attrs,function(k,v){                         // 循环属性字典
                $(sel).attr(k,v);                               // 将属性添加到select标签上
            });
            $.each(csses,function(k,v){                         // 将字典中的样式添加到select上
                $(sel).css(k,v);
            });
            $.each(options,function(k,v){                       // 循环一个option的字典  k为每个字典的key v为每个字典的value 此value也是一个字典
                var opt1=document.createElement('option');      // 创建一个option

                var sel_text = v[key_text];                     // 索引为key_text对应的值
                var sel_value = v[key_value];                   // 取出value字典中的id的值

                if(sel_text==current){                          // 判断字典中的name的值 是否等于标签中的文本
                    $(opt1).text(sel_text).attr('value', sel_value).attr('text', sel_text).attr('selected',true).appendTo($(sel));  // 将这个option设置了属性和内容之后追加到上面创建的selec标签中
                }else{
                    $(opt1).text(sel_text).attr('value', sel_value).attr('text', sel_text).appendTo($(sel));
                }
            });
            return sel;             // 将创建的这个select标签返回
        },


        /*
         搜索插件 -> 添加搜索条件
         ths:点击的当前对象
         */
        'AddSearchCondition':function(ths){

            var $duplicate = $(ths).parent().parent().clone(true);
            $duplicate.find('.icon-plus-sign').addClass('icon-minus-sign').removeClass('icon-plus-sign');
            $duplicate.find('a[onclick="$.AddSearchCondition(this)"]').attr('onclick',"$.RemoveSearchCondition(this)");

            $duplicate.appendTo($(ths).parent().parent().parent());
        },

        /*
         搜索插件 -> 移除当前搜索条件
         ths:点击的当前对象
         */
        'RemoveSearchCondition':function(ths){
            $(ths).parent().parent().remove();
        },

        'Hide':function(target){                // 向标签添加一个样式 hide
			$(target).addClass('hide');
		},

        'Show':function(target){
			$(target).removeClass('hide');
		},
        /*
         表格CheckBox全选
         tableBody:表格中body选择器对象
         rowEditFunc:行进入编辑模式的特殊函数处理，例如：状态、等不同的样式
         */

        'AllCheckedTr':function(tableBody){
            var check_tr_list = [];
            $(tableBody).find(':checkbox').each(function(){
                var check = $(this).prop('checked');
                var $tr = $(this).parent().parent();
                if(check){
                    check_tr_list.push($tr.attr('row-num'));
                }
            });
            return check_tr_list;

		},

        'CheckAll':function(tableBody,specialInEditFunc){

            if($(tableBody).attr('edit-mode')=='true'){
                $(tableBody).find(':checkbox').each(function(){
                    var check = $(this).prop('checked');
                    var $tr = $(this).parent().parent();
                    if(!check){
                        $tr.addClass('success');
                        DoTrIntoEdit($tr, specialInEditFunc);
                    }
                });
            }
            $(tableBody).find(':checkbox').prop('checked',true);
		},

        /*
         表格CheckBox取消选择
         tableBody:表格中body选择器对象
         */
		'UnCheckAll':function(tableBody, specialOutEditFunc){


            if($(tableBody).attr('edit-mode')=='true') {
                $(tableBody).find(':checkbox').each(function(){
                    var check = $(this).prop('checked');
                    var $tr = $(this).parent().parent();
                    if(check){
                        $tr.removeClass('success');
                        DoTrOutEdit($tr, specialOutEditFunc);
                    }
                });
            }

            $(tableBody).find(':checkbox').prop('checked',false);
		},

        /*
         表格CheckBox反选
         targetContainer:表格中body选择器对象
         specialInEditFunc:
         specialOutEditFunc:
         */
		'ReverseCheck':function(tableBody, specialInEditFunc, specialOutEditFunc){
			$(tableBody).find(':checkbox').each(function(){
				var check = $(this).prop('checked');
                var $tr = $(this).parent().parent();
				if(check){
					$(this).prop('checked',false);

                    if($(tableBody).attr('edit-mode')=='true'){
                        $tr.removeClass('success');
                        DoTrOutEdit($tr, specialOutEditFunc);
                    }


				}else{
					$(this).prop('checked',true);

                    if($(tableBody).attr('edit-mode')=='true'){
                        $tr.addClass('success');
                        //this row enable edit
                        DoTrIntoEdit($tr, specialInEditFunc);
                    }

				}
			})
		},

        /*
         绑定点击CheckBox事件
         targetContainer:表格中body选择器对象
         specialInEditFunc:
         specialOutEditFunc:
         给body下的所有checkbox绑定click执行事件
         先获取到每一行的资产数据
         根据checkbox是否被选中 以及根据body中的编辑属性是否为true来操作
         如果body的编辑属性为true 那么当点击checkbox时会触发事件
         如果选中 则进入编辑模式  如果没有选中 则退出编辑模式
         */
        'BindDoSingleCheck':function(tableBody, specialInEditFunc, specialOutEditFun){
            $(tableBody).find(':checkbox').bind('click',function(){     //  找到tbody下的所有的checkbox标签，并绑定一个click事件
                var $tr = $(this).parent().parent();        //  获取到这一行的tr所有数据
                if($(this).prop('checked')){                // 判断checkbox是否选中
                    if($(tableBody).attr('edit-mode')=='true'){             // 判断body的edit-mode属性是否为true
                        //this row switch in edit mode
                        $tr.addClass('success');                            // 向其添加一个success样式
                        DoTrIntoEdit($tr, specialInEditFunc);               // 进入编辑模式
                    }
                }else{
                    if($(tableBody).attr('edit-mode')=='true'){
                        //this row switch out edit mode
                        $tr.removeClass('success');
                        DoTrOutEdit($tr, specialOutEditFun);            // specialOutEditFun默认为空
                    }
                }

            });
        },

        /*
        表格排序
        header:表格中header选择器对象
        body:表格中body选择器对象
         */
        /*
        1、先将header里面的click事件移除
        2、再次绑定新的click事件，并定义新的触发事件函数
        3、将每一条资产数据都保存在一个列表里
        4、根据点击标签的索引值 将点击的某个标签下的所有文本和对应的资产的索引生成字典添加到一个列表中
        5、点击某个thead中的标签时，会根据标签中的样式来做出排序。排序的内容为点击标签所在列下的所有文本
        6、排序之后返回的是一个包含id和一个字典的数组 这个字典是关键取值
        7、根据返回的字典中的key 去第3步的资产列表中获取数据。并添加到body的标签下
        8、将新的body数据传给处理编辑模式的函数
        */
        'BindTableSort':function(header,body){                  // #table-head   #table-body
            $(header).find("th[en-sort='true']").unbind('click');               // 先移除click事件
            $(header).find("th[en-sort='true']").bind('click',function(){       // 找到所有符合条件的标签 在绑定一个事件
                                                                                // 当点击标签时 会触发事件 显示索引值
                var currentIndex = $(this).index();                             // 是点击某个排序标签时 这个标签在thead所有标签列表中的索引值
                //console.log(currentIndex);                              // 这里的$(this) 是点击的那个排序标签
                var originList = [];                            // 专门用来存放tr的列表
                var keyValueList = [];                          // 专门用来存放点击标签下 这一列的数据列表
                $(body).children().each(function(k,v){                          // 循环表格中的每一条资产数据 就是每一条tr
                    //console.log(k,v);                                    // k为这个tr在所有tr列表中的索引值 v为一个tr标签的所有内容
                    // 1. 将一行数据转换为jquery对象后添加到列表中
                    // 2. 取出点击标签下 所有的td中索引值相等的td的值
                    // 3. 将这些值存放在列表中
                    originList.push($(v));                             // v 是每一条tr的html标签，转换为jquery的对象后 添加到列表中
                    var currentData = $(this).children().eq(currentIndex).text();   // 点击某个排序标签后 取出这个被点击标签下 tr下的td列表中 索引值相等的内容
                    keyValueList.push({'key':k,'value':currentData});           // k为资产的索引值， currentData为个tr下对应索引值的td值
                });

                if($(this).hasClass('both')){         //  $(this) 是thead中点击的标签 当标签存在样式both时 说明是激活第一次排序 是降序 从大到小
                    //Asc排序         添加和删除样式   当第一次点击标签时 先移除both 样式 在添加一个desc样式 同时兄弟标签移除 asc 或desc后 添加both样式
                    $(this).removeClass('both').addClass('desc').siblings().removeClass('asc desc').addClass('both');
                    var sorted = SortDesc(keyValueList.length,keyValueList);        // 将这个列表进行排序
                }else if($(this).hasClass('desc')){             // 当点击的标签存在样式desc时  说明要激活 升序  从小到大
                    //Desc排序
                    $(this).removeClass('desc').addClass('asc').siblings().removeClass('asc desc').addClass('both');
                    var sorted = SortAsc(keyValueList.length,keyValueList);

                }else if($(this).hasClass('asc')){          // 当点击的标签存在asc时 需要激活升序
                    //Asc排序
                    $(this).removeClass('asc').addClass('desc').siblings().removeClass('asc desc').addClass('both');
                    var sorted = SortDesc(keyValueList.length,keyValueList);
                }
                if(sorted){     //  sorted为排序后返回的列表 其中每个元素里都包含两个子元素。 id 和 {key: 1, value: "56JRZ42"}
                    $(body).empty();        // 先将body制空
                    $.each(sorted,function(k,v){                // 循环已经排序OK 的列表 v 为列表中的每一个值
                        $(body).append(originList[v.key]);      // 根据排序的数组中的key 依次去原数据的列表中取出数据 添加到body标签下
                    });
                    $.BindDoSingleCheck(body);
                }

            })
		},
        /*
        重置排序
         */
        'ResetTableSort':function(header,body){         // 对thead做一些样式的修改
            $(header).find("th[en-sort='true']").removeClass('desc asc').addClass('both');
        },

        /*
        表格进入编辑模式
        ths:编辑模式这个按钮
        body: #table-body标签
         */
        'IntoEditMode':function(ths,body, specialInEditFunc, specialOutEditFunc){
            if($(ths).hasClass('in-editing')){                 // 正处于编辑模式，点击将退出编辑模式
                $(ths).removeClass('in-editing').text('进入编辑模式');
                $(body).attr('edit-mode','false');
                $(body).children().removeClass('success');      // 将一个tr的标签 移除success样式
                $(body).find(':checkbox').each(function(){      // 循环所有的checkbox
                    var check = $(this).prop('checked');        // 获取checkbox的选中状态
                    var $tr = $(this).parent().parent();
                    if(check){                                  // 当状态为选中时
                        $tr.removeClass('success');             // tr移除success样式
                        DoTrOutEdit($tr, specialOutEditFunc);
                    }
                });
                //all unable edit

            }else{                                                 // 正处于非编辑模式，点击将进入编辑模式
                //into edit mode
                $(ths).addClass('in-editing').text('退出编辑模式');
                $(body).attr('edit-mode','true');
                $(body).find(':checkbox').each(function(){
                    console.log("-----------------");
                    var check = $(this).prop('checked');            // 获取checkbox的状态 选中 或者未选中
                    var $tr = $(this).parent().parent();            // 这是一行数据   一个 tr
                    console.log("111111111111111111111111");
                    if(check){                                      // 如果checkbox被选中
                        $tr.addClass('success');                    // 添加一个 success样式
                        console.log("2222222222222222222222222222");
                        DoTrIntoEdit($tr, specialInEditFunc);
                    }
                });
            }
        },

        /*
        tab菜单(例如：$.BindTabMenu('#tab-menu-title', '#tab-menu-body');)
         */
        'BindTabMenu':function(title, body) {
            $(title).children().bind("click", function () {
                var $menu = $(this);
                var $content = $(body).find('div[content="' + $(this).attr("content-to") + '"]');
                $menu.addClass('current').siblings().removeClass('current');
                $content.removeClass('hide').siblings().addClass('hide');
            });
        }
    });
})(jQuery);