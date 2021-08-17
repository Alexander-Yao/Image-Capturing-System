/**
 * @ignore
 */
/*
 * Your about ViewModel code goes here
 */
define(['accUtils'],
 function(accUtils) {
    function AboutViewModel() {
        layui.use(function () {
            $ = layui.$
                , layer = layui.layer
                , form = layui.form
                , laypage = layui.laypage
                , element = layui.element
                , laydate = layui.laydate
                , util = layui.util;


            /**
             * get map button
             */
            form.on('submit(demo11)', function (data) {
                console.log(data.elem) //The element DOM object of the event being executed, generally a button object
                console.log(data.form) //The form object submitted by execution will generally be returned when there is a form tag
                console.log(data.field) //All form fields of the current container, in the form of name-value pairs: {name: value}
                $.ajax({
                    url: 'http://127.0.0.1:5000/pic',
                    datatype: 'json',
                    type: 'get',
                    crossDomain: true,
                    data: "lon=" + data.field.lon + "&lat= " + data.field.lat + "&tileZoom= " + data.field.tileZoom,
                    success: function (data) {
                        console.log(data);

                        var str = '';
                        //Google
                        str += '<div class="layui-col-xs4 layui-col-sm4 layui-col-md4">';
                        str += '<p>Bing</p>';
                        str += '<img src=../' + data.bing + '>';
                        str += '</div>';
                        //BIng

                        str += '<div class="layui-col-xs4 layui-col-sm4 layui-col-md4">';
                        str += '<p>Google</p>';
                        str += '<img src=../' + data.google + '>';
                        str += '</div>';
                        //OSM
                        str += '<div class="layui-col-xs4 layui-col-sm4 layui-col-md4">';
                        str += '<p>OSM</p>';
                        str += '<img src=../' + data.osm + '>';
                        str += '</div>';


                        $("#test1").append(str);


                    }
                });
                return false; //Prevent form redirection. If you need to jump to the form, just remove this paragraph.

            });


            /**
             * zoom in
             */

            form.on('submit(demo12)', function (data) {

                $.ajax({
                    url: 'http://127.0.0.1:5000/multi',
                    datatype: 'json',
                    type: 'get',
                    crossDomain: true,
                    data: "lon=" + data.field.lon + "&lat= " + data.field.lat + "&tileZoom= " + data.field.tileZoom + "&multi=" + data.field.multi,
                    success: function (data) {
                        console.log(data)
                        let url = '?'
                        for (const key in data) {
                            url += key + '=' + data[key] + '&'
                        }
                        url = url.substr(0, url.length - 1);
                        location.href = "zoom.html" + url
                        /**
                        var str = ''
                        //Google
                        str += '<div class="layui-col-xs4 layui-col-sm4 layui-col-md4">';
                        str += '<p>Bing</p>';
                        str += '<img src=/' + data.bing + '>';
                        str += '</div>';
                        //BIng
        
                        str += '<div class="layui-col-xs4 layui-col-sm4 layui-col-md4">';
                        str += '<p>Google</p>';
                        str += '<img src=/' + res.goole + '>';
                        str += '</div>';
                        //OSM
                        str += '<div class="layui-col-xs4 layui-col-sm4 layui-col-md4">';
                        str += '<p>OSM</p>';
                        str += '<img src=/' + res.osm + '>';
                        str += '</div>';
        
                        $("#test2").append(str);
                         */

                    }
                })
                return false;
            });

        });
        // Below are a set of the ViewModel methods invoked by the oj-module component.
      // Please reference the oj-module jsDoc for additional information.

      /**
       * Optional ViewModel method invoked after the View is inserted into the
       * document DOM.  The application can put logic that requires the DOM being
       * attached here.
       * This method might be called multiple times - after the View is created
       * and inserted into the DOM and after the View is reconnected
       * after being disconnected.
       */
      this.connected = () => {
        accUtils.announce('About page loaded.', 'assertive');
        document.title = "About";
        // Implement further logic if needed
      };

      /**
       * Optional ViewModel method invoked after the View is disconnected from the DOM.
       */
      this.disconnected = () => {
        // Implement if needed
      };

      /**
       * Optional ViewModel method invoked after transition to the new View is complete.
       * That includes any possible animation between the old and the new View.
       */
      this.transitionCompleted = () => {
        // Implement if needed
      };
    }

    /*
     * Returns an instance of the ViewModel providing one instance of the ViewModel. If needed,
     * return a constructor for the ViewModel so that the ViewModel is constructed
     * each time the view is displayed.
     */
    return AboutViewModel;
  }
);
