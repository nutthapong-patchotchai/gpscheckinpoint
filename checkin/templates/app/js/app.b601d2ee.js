(function(e){function t(t){for(var n,a,s=t[0],c=t[1],u=t[2],l=0,m=[];l<s.length;l++)a=s[l],Object.prototype.hasOwnProperty.call(o,a)&&o[a]&&m.push(o[a][0]),o[a]=0;for(n in c)Object.prototype.hasOwnProperty.call(c,n)&&(e[n]=c[n]);p&&p(t);while(m.length)m.shift()();return i.push.apply(i,u||[]),r()}function r(){for(var e,t=0;t<i.length;t++){for(var r=i[t],n=!0,a=1;a<r.length;a++){var s=r[a];0!==o[s]&&(n=!1)}n&&(i.splice(t--,1),e=c(c.s=r[0]))}return e}var n={},a={app:0},o={app:0},i=[];function s(e){return c.p+"js/"+({}[e]||e)+"."+{"chunk-02588a14":"79a11fee","chunk-523b7b98":"b161c8c1","chunk-79af50a7":"7a651a23","chunk-7c360ba7":"7fd84356"}[e]+".js"}function c(t){if(n[t])return n[t].exports;var r=n[t]={i:t,l:!1,exports:{}};return e[t].call(r.exports,r,r.exports,c),r.l=!0,r.exports}c.e=function(e){var t=[],r={"chunk-02588a14":1,"chunk-523b7b98":1,"chunk-79af50a7":1,"chunk-7c360ba7":1};a[e]?t.push(a[e]):0!==a[e]&&r[e]&&t.push(a[e]=new Promise((function(t,r){for(var n="css/"+({}[e]||e)+"."+{"chunk-02588a14":"560fea89","chunk-523b7b98":"560fea89","chunk-79af50a7":"21626796","chunk-7c360ba7":"8b33d15c"}[e]+".css",o=c.p+n,i=document.getElementsByTagName("link"),s=0;s<i.length;s++){var u=i[s],l=u.getAttribute("data-href")||u.getAttribute("href");if("stylesheet"===u.rel&&(l===n||l===o))return t()}var m=document.getElementsByTagName("style");for(s=0;s<m.length;s++){u=m[s],l=u.getAttribute("data-href");if(l===n||l===o)return t()}var p=document.createElement("link");p.rel="stylesheet",p.type="text/css",p.onload=t,p.onerror=function(t){var n=t&&t.target&&t.target.src||o,i=new Error("Loading CSS chunk "+e+" failed.\n("+n+")");i.code="CSS_CHUNK_LOAD_FAILED",i.request=n,delete a[e],p.parentNode.removeChild(p),r(i)},p.href=o;var f=document.getElementsByTagName("head")[0];f.appendChild(p)})).then((function(){a[e]=0})));var n=o[e];if(0!==n)if(n)t.push(n[2]);else{var i=new Promise((function(t,r){n=o[e]=[t,r]}));t.push(n[2]=i);var u,l=document.createElement("script");l.charset="utf-8",l.timeout=120,c.nc&&l.setAttribute("nonce",c.nc),l.src=s(e);var m=new Error;u=function(t){l.onerror=l.onload=null,clearTimeout(p);var r=o[e];if(0!==r){if(r){var n=t&&("load"===t.type?"missing":t.type),a=t&&t.target&&t.target.src;m.message="Loading chunk "+e+" failed.\n("+n+": "+a+")",m.name="ChunkLoadError",m.type=n,m.request=a,r[1](m)}o[e]=void 0}};var p=setTimeout((function(){u({type:"timeout",target:l})}),12e4);l.onerror=l.onload=u,document.head.appendChild(l)}return Promise.all(t)},c.m=e,c.c=n,c.d=function(e,t,r){c.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},c.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},c.t=function(e,t){if(1&t&&(e=c(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(c.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var n in e)c.d(r,n,function(t){return e[t]}.bind(null,n));return r},c.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return c.d(t,"a",t),t},c.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},c.p="/static/",c.oe=function(e){throw console.error(e),e};var u=window["webpackJsonp"]=window["webpackJsonp"]||[],l=u.push.bind(u);u.push=t,u=u.slice();for(var m=0;m<u.length;m++)t(u[m]);var p=l;i.push([0,"chunk-vendors"]),r()})({0:function(e,t,r){e.exports=r("56d7")},"56d7":function(e,t,r){"use strict";r.r(t);r("e260"),r("e6cf"),r("cca6"),r("a79d");var n=r("2b0e"),a=(r("d3b7"),r("bc3a")),o=r.n(a),i={baseURL:Object({NODE_ENV:"production",BASE_URL:"/static/"}).baseURL||Object({NODE_ENV:"production",BASE_URL:"/static/"}).apiUrl||"https://dorm.dsq.up.ac.th"},s=o.a.create(i);s.interceptors.request.use((function(e){return e}),(function(e){return Promise.reject(e)})),s.interceptors.response.use((function(e){return e}),(function(e){return Promise.reject(e)}));var c=s,u=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{attrs:{id:"app"}},[r("router-view")],1)},l=[],m=(r("96cf"),r("1da1")),p={name:"Root",components:{},props:{},data:function(){return{txt:"Hello World"}},mounted:function(){var e=Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,this.load();case 2:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}(),beforeRouteEnter:function(e,t,r){return Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:r();case 1:case"end":return e.stop()}}),e)})))()},computed:{},methods:{load:function(){var e=Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:case"end":return e.stop()}}),e)})));function t(){return e.apply(this,arguments)}return t}()}},f=p,d=r("2877"),h=Object(d["a"])(f,u,l,!1,null,null,null),v=h.exports,b=r("8c4f"),g=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("Navbar"),r("router-view"),r("Footers")],1)},x=[],w=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("nav",{staticClass:"fixed z-50 w-full flex items-center justify-between flex-wrap bg-white p-6"},[e._m(0),r("div",{staticClass:"block sm:hidden"},[r("button",{staticClass:"flex items-center px-3 py-2 border rounded text-teal-lighter border-teal-light text-purple-600 hover:text-purple-300 hover:border-white",on:{click:e.toggle}},[r("svg",{staticClass:"fill-current h-3 w-3",attrs:{viewBox:"0 0 20 20",xmlns:"http://www.w3.org/2000/svg"}},[r("title",[e._v("Menu")]),r("path",{attrs:{d:"M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"}})])])]),r("div",{staticClass:"w-full flex-grow sm:flex sm:items-center sm:w-auto",class:e.open?"block":"hidden"},[e._m(1),e._m(2)])])])},k=[function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"flex items-center flex-no-shrink text-white mr-6"},[r("img",{staticClass:"h-16",attrs:{src:"https://www.img.in.th/images/8709fe5d9cfbe80098ce862c8ce291b8.png",alt:""}})])},function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"text-sm sm:flex-grow"},[r("a",{staticClass:"no-underline block mt-4 sm:inline-block sm:mt-0 text-teal-lighter hover:text-purple-300  text-lg mr-4 ml-4",attrs:{href:"#responsive-header"}},[e._v(" หน้าแรก ")]),r("a",{staticClass:"no-underline block mt-4 sm:inline-block sm:mt-0 text-teal-lighter hover:text-purple-300   text-lg mr-4",attrs:{href:"#responsive-header"}},[e._v(" หอพัก ")]),r("a",{staticClass:"no-underline block mt-4 sm:inline-block sm:mt-0 text-teal-lighter hover:text-purple-300   text-lg mr-4",attrs:{href:"#responsive-header"}},[e._v(" แผนที่โซน ")]),r("a",{staticClass:"no-underline block mt-4 sm:inline-block sm:mt-0 text-teal-lighter hover:text-purple-300  text-lg mr-4",attrs:{href:"#responsive-header"}},[e._v(" เกี่ยวกับ ")])])},function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("a",{staticClass:"no-underline inline-block text-sm px-4 py-2 leading-none border rounded text-purple-600 border-purple-600 hover:border-purple-300 hover:text-teal hover:bg-white mt-4 sm:mt-0",attrs:{href:"https://dorm.dsq.up.ac.th/checkin/#/"}},[e._v(" UP CHECKIN ")])])}],C={name:"Root",components:{},props:{},data:function(){return{open:!1,txt:"Hello World"}},mounted:function(){var e=Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,this.load();case 2:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}(),beforeRouteEnter:function(e,t,r){return Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:r();case 1:case"end":return e.stop()}}),e)})))()},computed:{},methods:{toggle:function(){this.open=!this.open},load:function(){var e=Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:case"end":return e.stop()}}),e)})));function t(){return e.apply(this,arguments)}return t}()}},y=C,R=Object(d["a"])(y,w,k,!1,null,"7b599d5e",null),_=R.exports,O=function(){var e=this,t=e.$createElement;e._self._c;return e._m(0)},j=[function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("footer",{staticClass:"w-full text-center border-t border-grey p-4 pin-b"},[r("div",{staticClass:"container mx-auto  px-8"},[r("div",{staticClass:"w-full flex flex-col md:flex-row py-6"},[r("div",{staticClass:"flex-1 mb-6"},[r("img",{attrs:{src:"https://www.img.in.th/images/8709fe5d9cfbe80098ce862c8ce291b8.png",alt:""}}),r("p",{staticClass:"p-4"},[e._v(" หน่วยหอพัก กองกิจการนิสิต "),r("br"),e._v(" มหาวิทยาลัยพะเยา"),r("br"),e._v(" 19 หมู่ 2 ต.แม่กา อ.เมือง"),r("br"),e._v(" จ.พะเยา 56000"),r("br"),e._v(" โทร: 054-466666 ต่อ 1071 ")])]),r("div",{staticClass:"flex-1"},[r("p",{staticClass:"uppercase text-gray-500 md:mb-6"},[e._v("Links")]),r("ul",{staticClass:"list-reset mb-6"},[r("li",{staticClass:"mt-2 inline-block mr-2 md:block md:mr-0"},[r("a",{staticClass:"no-underline hover:underline text-gray-800 hover:text-orange-500",attrs:{href:"#"}},[e._v("FAQ")])]),r("li",{staticClass:"mt-2 inline-block mr-2 md:block md:mr-0"},[r("a",{staticClass:"no-underline hover:underline text-gray-800 hover:text-orange-500",attrs:{href:"#"}},[e._v("Help")])]),r("li",{staticClass:"mt-2 inline-block mr-2 md:block md:mr-0"},[r("a",{staticClass:"no-underline hover:underline text-gray-800 hover:text-orange-500",attrs:{href:"#"}},[e._v("Support")])])])]),r("div",{staticClass:"flex-1"},[r("p",{staticClass:"uppercase text-gray-500 md:mb-6"},[e._v("Legal")]),r("ul",{staticClass:"list-reset mb-6"},[r("li",{staticClass:"mt-2 inline-block mr-2 md:block md:mr-0"},[r("a",{staticClass:"no-underline hover:underline text-gray-800 hover:text-orange-500",attrs:{href:"#"}},[e._v("Terms")])]),r("li",{staticClass:"mt-2 inline-block mr-2 md:block md:mr-0"},[r("a",{staticClass:"no-underline hover:underline text-gray-800 hover:text-orange-500",attrs:{href:"#"}},[e._v("Privacy")])])])]),r("div",{staticClass:"flex-1"},[r("p",{staticClass:"uppercase text-gray-500 md:mb-6"},[e._v("Social")]),r("ul",{staticClass:"list-reset mb-6"},[r("li",{staticClass:"mt-2 inline-block mr-2 md:block md:mr-0"},[r("a",{staticClass:"no-underline hover:underline text-gray-800 hover:text-orange-500",attrs:{href:"#"}},[e._v("Facebook")])]),r("li",{staticClass:"mt-2 inline-block mr-2 md:block md:mr-0"},[r("a",{staticClass:"no-underline hover:underline text-gray-800 hover:text-orange-500",attrs:{href:"#"}},[e._v("Linkedin")])]),r("li",{staticClass:"mt-2 inline-block mr-2 md:block md:mr-0"},[r("a",{staticClass:"no-underline hover:underline text-gray-800 hover:text-orange-500",attrs:{href:"#"}},[e._v("Twitter")])])])]),r("div",{staticClass:"flex-1"},[r("p",{staticClass:"uppercase text-gray-500 md:mb-6"},[e._v("Company")]),r("ul",{staticClass:"list-reset mb-6"},[r("li",{staticClass:"mt-2 inline-block mr-2 md:block md:mr-0"},[r("a",{staticClass:"no-underline hover:underline text-gray-800 hover:text-orange-500",attrs:{href:"#"}},[e._v("Official Blog")])]),r("li",{staticClass:"mt-2 inline-block mr-2 md:block md:mr-0"},[r("a",{staticClass:"no-underline hover:underline text-gray-800 hover:text-orange-500",attrs:{href:"#"}},[e._v("About Us")])]),r("li",{staticClass:"mt-2 inline-block mr-2 md:block md:mr-0"},[r("a",{staticClass:"no-underline hover:underline text-gray-800 hover:text-orange-500",attrs:{href:"#"}},[e._v("Contact")])])])])])])])}],E={name:"Root",components:{},props:{},data:function(){return{txt:"Hello World"}},mounted:function(){var e=Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,this.load();case 2:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}(),beforeRouteEnter:function(e,t,r){return Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:r();case 1:case"end":return e.stop()}}),e)})))()},computed:{},methods:{load:function(){var e=Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:case"end":return e.stop()}}),e)})));function t(){return e.apply(this,arguments)}return t}()}},S=E,H=Object(d["a"])(S,O,j,!1,null,"791440f8",null),P=H.exports,A={name:"Root",components:{Navbar:_,Footers:P},props:{},data:function(){return{txt:"Hello World"}},mounted:function(){var e=Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,this.load();case 2:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}(),beforeRouteEnter:function(e,t,r){return Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:r();case 1:case"end":return e.stop()}}),e)})))()},computed:{},methods:{load:function(){var e=Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:case"end":return e.stop()}}),e)})));function t(){return e.apply(this,arguments)}return t}()}},L=A,N=Object(d["a"])(L,g,x,!1,null,"057fe46f",null),D=N.exports,T=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("router-view")],1)},$=[],U={name:"Root",components:{},props:{},data:function(){return{txt:"Hello World"}},mounted:function(){var e=Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,this.load();case 2:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}(),beforeRouteEnter:function(e,t,r){return Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:r();case 1:case"end":return e.stop()}}),e)})))()},computed:{},methods:{load:function(){var e=Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:case"end":return e.stop()}}),e)})));function t(){return e.apply(this,arguments)}return t}()}},B=U,M=Object(d["a"])(B,T,$,!1,null,"64e02cef",null),z=M.exports;n["default"].use(b["a"]);var V=[{path:"/",component:D,children:[{path:"",name:"Root-Home",component:function(){return r.e("chunk-79af50a7").then(r.bind(null,"5d8a"))}},{path:"test",name:"Root-test",component:function(){return r.e("chunk-523b7b98").then(r.bind(null,"4c72"))}}]},{path:"/admin",component:z,children:[{path:"",name:"Admin-Home",component:function(){return r.e("chunk-7c360ba7").then(r.bind(null,"3c19"))}},{path:"test",name:"Admin-test",component:function(){return r.e("chunk-02588a14").then(r.bind(null,"f4fc"))}}]}],q=new b["a"]({routes:V}),F=q,I=r("2f62"),W=r("7ffd"),Z=(r("2ef0"),{testVar:{}}),J={},K=W["c"].mutations(Z),Q={storeDorm:function(e,t){return Object(m["a"])(regeneratorRuntime.mark((function e(){var r;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.post("/api/dorm/dorm/",t).then((function(e){return e.data}))["catch"]((function(e){return!1}));case 2:return r=e.sent,e.abrupt("return",r);case 4:case"end":return e.stop()}}),e)})))()},storeDormOwner:function(e,t){return Object(m["a"])(regeneratorRuntime.mark((function e(){var r;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.post("/api/dorm/dormowner/",t).then((function(e){return e.data}))["catch"]((function(e){return!1}));case 2:return r=e.sent,e.abrupt("return",r);case 4:case"end":return e.stop()}}),e)})))()},storeDormDetail:function(e,t){return Object(m["a"])(regeneratorRuntime.mark((function e(){var r;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.post("/api/dorm/dormdetail/",t).then((function(e){return e.data}))["catch"]((function(e){return!1}));case 2:return r=e.sent,e.abrupt("return",r);case 4:case"end":return e.stop()}}),e)})))()},storeDormStyle:function(e,t){return Object(m["a"])(regeneratorRuntime.mark((function e(){var r;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.post("/api/dorm/dormstyle/",t).then((function(e){return e.data}))["catch"]((function(e){return!1}));case 2:return r=e.sent,e.abrupt("return",r);case 4:case"end":return e.stop()}}),e)})))()},testApi:function(e,t){return Object(m["a"])(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.get("/user/login").then((function(e){}))["catch"]((function(e){}));case 2:case"end":return e.stop()}}),e)})))()}},G={namespaced:!0,state:Z,getters:J,mutations:K,actions:Q},X={testVar:{},SIZES:[]},Y={},ee=W["c"].mutations(X),te={getMetadata:function(e,t){return Object(m["a"])(regeneratorRuntime.mark((function e(){var r;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.get("/api/dorm/choice/?name=".concat(t)).then((function(e){return e.data}))["catch"]((function(e){return e.response.data}));case 2:return r=e.sent,e.abrupt("return",r);case 4:case"end":return e.stop()}}),e)})))()},getSize:function(e,t){return Object(m["a"])(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.get("/api/size").then((function(e){return e.data}))["catch"]((function(e){return alert("Error"),e.response.data}));case 2:return t=e.sent,X.SIZES=t,e.abrupt("return",t);case 5:case"end":return e.stop()}}),e)})))()},getHomeDorm:function(e,t){return Object(m["a"])(regeneratorRuntime.mark((function e(){var t;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,c.get("/api/dorm/dorm/home/").then((function(e){return e.data}))["catch"]((function(e){return alert("Error"),e.response.data}));case 2:return t=e.sent,X.SIZES=t,e.abrupt("return",t);case 5:case"end":return e.stop()}}),e)})))()}},re={namespaced:!0,state:X,getters:Y,mutations:ee,actions:te};n["default"].use(I["a"]);var ne=function(){var e=new I["a"].Store({plugins:[W["b"].plugin],modules:{test:G,home:re}});return e},ae=r("574d"),oe=r.n(ae);r("04f2");n["default"].use(oe.a,{}),n["default"].config.productionTip=!1,new n["default"]({router:F,store:ne,render:function(e){return e(v)}}).$mount("#app")}});
//# sourceMappingURL=app.b601d2ee.js.map