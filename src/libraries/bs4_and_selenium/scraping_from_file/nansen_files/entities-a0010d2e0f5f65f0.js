(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[791],{46901:function(e,t,r){"use strict";r.d(t,{Z:function(){return E}});var n=r(63366),i=r(87462),o=r(67294),a=r(86010),s=r(27192),c=r(41796),l=r(11496),u=r(71657),d=r(98216),p=r(55113),f=r(28979);function m(e){return(0,f.Z)("MuiAlert",e)}var h,g=(0,r(76087).Z)("MuiAlert",["root","action","icon","message","filled","filledSuccess","filledInfo","filledWarning","filledError","outlined","outlinedSuccess","outlinedInfo","outlinedWarning","outlinedError","standard","standardSuccess","standardInfo","standardWarning","standardError"]),v=r(93946),x=r(82066),j=r(85893),y=(0,x.Z)((0,j.jsx)("path",{d:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2, 4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0, 0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"}),"SuccessOutlined"),b=(0,x.Z)((0,j.jsx)("path",{d:"M12 5.99L19.53 19H4.47L12 5.99M12 2L1 21h22L12 2zm1 14h-2v2h2v-2zm0-6h-2v4h2v-4z"}),"ReportProblemOutlined"),O=(0,x.Z)((0,j.jsx)("path",{d:"M11 15h2v2h-2zm0-8h2v6h-2zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"}),"ErrorOutline"),Z=(0,x.Z)((0,j.jsx)("path",{d:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"}),"InfoOutlined"),w=r(34484);const k=["action","children","className","closeText","color","icon","iconMapping","onClose","role","severity","variant"],P=(0,l.ZP)(p.Z,{name:"MuiAlert",slot:"Root",overridesResolver:(e,t)=>{const{ownerState:r}=e;return[t.root,t[r.variant],t[`${r.variant}${(0,d.Z)(r.color||r.severity)}`]]}})((({theme:e,ownerState:t})=>{const r="light"===e.palette.mode?c._j:c.$n,n="light"===e.palette.mode?c.$n:c._j,o=t.color||t.severity;return(0,i.Z)({},e.typography.body2,{backgroundColor:"transparent",display:"flex",padding:"6px 16px"},o&&"standard"===t.variant&&{color:r(e.palette[o].light,.6),backgroundColor:n(e.palette[o].light,.9),[`& .${g.icon}`]:{color:"dark"===e.palette.mode?e.palette[o].main:e.palette[o].light}},o&&"outlined"===t.variant&&{color:r(e.palette[o].light,.6),border:`1px solid ${e.palette[o].light}`,[`& .${g.icon}`]:{color:"dark"===e.palette.mode?e.palette[o].main:e.palette[o].light}},o&&"filled"===t.variant&&{color:"#fff",fontWeight:e.typography.fontWeightMedium,backgroundColor:"dark"===e.palette.mode?e.palette[o].dark:e.palette[o].main})})),S=(0,l.ZP)("div",{name:"MuiAlert",slot:"Icon",overridesResolver:(e,t)=>t.icon})({marginRight:12,padding:"7px 0",display:"flex",fontSize:22,opacity:.9}),C=(0,l.ZP)("div",{name:"MuiAlert",slot:"Message",overridesResolver:(e,t)=>t.message})({padding:"8px 0"}),M=(0,l.ZP)("div",{name:"MuiAlert",slot:"Action",overridesResolver:(e,t)=>t.action})({display:"flex",alignItems:"flex-start",padding:"4px 0 0 16px",marginLeft:"auto",marginRight:-8}),A={success:(0,j.jsx)(y,{fontSize:"inherit"}),warning:(0,j.jsx)(b,{fontSize:"inherit"}),error:(0,j.jsx)(O,{fontSize:"inherit"}),info:(0,j.jsx)(Z,{fontSize:"inherit"})};var E=o.forwardRef((function(e,t){const r=(0,u.Z)({props:e,name:"MuiAlert"}),{action:o,children:c,className:l,closeText:p="Close",color:f,icon:g,iconMapping:x=A,onClose:y,role:b="alert",severity:O="success",variant:Z="standard"}=r,E=(0,n.Z)(r,k),z=(0,i.Z)({},r,{color:f,severity:O,variant:Z}),_=(e=>{const{variant:t,color:r,severity:n,classes:i}=e,o={root:["root",`${t}${(0,d.Z)(r||n)}`,`${t}`],icon:["icon"],message:["message"],action:["action"]};return(0,s.Z)(o,m,i)})(z);return(0,j.jsxs)(P,(0,i.Z)({role:b,elevation:0,ownerState:z,className:(0,a.default)(_.root,l),ref:t},E,{children:[!1!==g?(0,j.jsx)(S,{ownerState:z,className:_.icon,children:g||x[O]||A[O]}):null,(0,j.jsx)(C,{ownerState:z,className:_.message,children:c}),null!=o?(0,j.jsx)(M,{className:_.action,children:o}):null,null==o&&y?(0,j.jsx)(M,{ownerState:z,className:_.action,children:(0,j.jsx)(v.Z,{size:"small","aria-label":p,title:p,color:"inherit",onClick:y,children:h||(h=(0,j.jsx)(w.Z,{fontSize:"small"}))})}):null]}))}))},34484:function(e,t,r){"use strict";r(67294);var n=r(82066),i=r(85893);t.Z=(0,n.Z)((0,i.jsx)("path",{d:"M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"}),"Close")},59480:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return R}});var n=r(82192),i=r(99226),o=r(15861),a=r(46901),s=r(50122),c=r(67294),l=r(46230),u=r(24773),d=r(81519),p=r(37021),f=r(59499),m=r(50029),h=r(16835),g=r(4730),v=r(87794),x=r.n(v),j=r(83287),y=r(66242),b=r(26447),O=r(11057),Z=r(71217),w=r(11163),k=r(56254),P=r(15109),S=r(24737),C=r(608),M=r(6001),A=r(2358),E=r(85893),z=["fund"];function _(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function D(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?_(Object(r),!0).forEach((function(t){(0,f.Z)(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):_(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}var L=(0,Z.Pi)((function(e){var t=e.fund,r=(0,g.Z)(e,z),n=(0,w.useRouter)(),a=(0,k.Ds)().enqueueSnackbar,s=(0,P.Z)((0,m.Z)(x().mark((function e(){return x().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return u.z.track({name:"[Fund] - Import",properties:{fund:t.name}}),e.next=3,C._.create({name:t.name,protocols:t.protocols,wallets:t.wallets});case 3:a((0,E.jsxs)("span",{children:["Added ",(0,E.jsx)("b",{children:t.name})," to your portfolio"]}),{variant:"success"});case 4:case"end":return e.stop()}}),e)}))),[a,t]),d=(0,h.Z)(s,2),p=d[0].loading,f=d[1],v=(0,c.useCallback)((function(){u.z.track({name:"[Fund] - View",properties:{fund:t.name}}),S.Z.peek({address:t.id,protocols:l.K.get(t.id).protocols}),n.push("/dashboard/".concat(t.id))}),[n,t]);return(0,E.jsx)(y.Z,D(D({},r),{},{sx:D({p:2,pt:4},r.sx),children:(0,E.jsxs)(i.Z,{display:"flex",flexDirection:"column",alignItems:"center",children:[(0,E.jsx)(A.w,{src:t.logo,size:64,borderRadius:"50%",sx:{objectFit:"covert",opacity:t.isEnabled?1:.5},mb:2}),(0,E.jsx)(o.Z,{variant:"caption",color:"text.secondary",gutterBottom:!0,children:"Entity"}),(0,E.jsx)(o.Z,{variant:"h4",color:t.isEnabled?"text.primary":"text.secondary",align:"center",mb:3,children:t.name}),t.isEnabled?(0,E.jsxs)(b.Z,{children:[M.H.firebaseUser&&(0,E.jsx)(j.Z,{variant:"contained",color:"primary",sx:{flexShrink:0},onClick:f,loading:p,loadingPosition:"start",startIcon:(0,E.jsx)(i.Z,{width:p?24:0}),children:p?"Saving...":"Add to Portfolio"}),(0,E.jsx)(O.Z,{variant:"outlined",onClick:v,children:"View"})]}):(0,E.jsx)(O.Z,{variant:"outlined",fullWidth:!0,href:"https://www.nansen.ai/institutions#institution_contact_form",target:"_blank",rel:"noopener",onClick:function(){u.z.track({name:"[Fund] - Contact",properties:{fund:t.name}})},children:"Contact Us"})]})}))}));var I=(0,n.Z)(i.Z,{target:"e87b8k70"})({name:"1gs3ii",styles:"display:grid;grid-template-columns:repeat(auto-fill, minmax(min(230px, 100%), 1fr));gap:1rem"}),R=function(){var e=(0,c.useMemo)((function(){var e=Array.from(l.K.values());return[{name:"Exchange Holdings",entities:e.filter((function(e){return"exchange"===e.category}))},{name:"DeFi",entities:e.filter((function(e){return"defi"===e.category}))},{name:"DAOs",entities:e.filter((function(e){return"dao"===e.category}))},{name:"Funds",entities:e.filter((function(e){return"fund"===e.category}))}].filter((function(e){return e.entities.length>0}))}),[]);return(0,E.jsxs)(E.Fragment,{children:[(0,E.jsx)(d.X,{children:(0,E.jsx)(o.Z,{variant:"h3",color:"text.primary",children:"Entities"})}),(0,E.jsxs)(p.c,{py:4,children:[(0,E.jsxs)(a.Z,{severity:"info",variant:"outlined",sx:{mb:3},children:["A curated list of well known Entities by Nansen. If your interested entities are missing, you can"," ",(0,E.jsx)(s.Z,{href:"https://docs.google.com/forms/d/e/1FAIpQLSeSWVF4VJ__V8z66TBiTuMW3eymY81Lp-r8sMVeRIFgpyGIwQ/viewform",target:"_blank",rel:"noopener",onClick:function(){u.z.track({name:"[Fund] - Request"})},children:"make a request"})," ","here!"]}),e.map((function(e){return(0,E.jsxs)(i.Z,{mb:4,children:[(0,E.jsx)(o.Z,{variant:"h3",color:"text.primary",mb:1,children:e.name}),(0,E.jsx)(I,{children:e.entities.filter((function(e){return!e.isHidden})).map((function(e){return(0,E.jsx)(L,{fund:e},e.id)}))})]},e.name)}))]})]})}},81519:function(e,t,r){"use strict";r.d(t,{X:function(){return s}});var n=r(59499),i=r(99226),o=r(85893);function a(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}var s=function(e){return(0,o.jsx)(i.Z,function(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?a(Object(r),!0).forEach((function(t){(0,n.Z)(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}({borderBottom:"1px solid",borderColor:"divider",minHeight:60,display:"flex",alignItems:"center",py:1,px:{xs:2,sm:3}},e))}},37021:function(e,t,r){"use strict";r.d(t,{c:function(){return s}});var n=r(59499),i=r(99226),o=r(85893);function a(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}var s=function(e){return(0,o.jsx)(i.Z,function(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?a(Object(r),!0).forEach((function(t){(0,n.Z)(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):a(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}({maxWidth:1040,mx:"auto",px:{xs:2,sm:3}},e))}},75702:function(e,t,r){(window.__NEXT_P=window.__NEXT_P||[]).push(["/entities",function(){return r(59480)}])},15109:function(e,t,r){"use strict";r.d(t,{Z:function(){return a}});var n=r(70655),i=r(67294),o=r(84956);function a(e,t,r){void 0===t&&(t=[]),void 0===r&&(r={loading:!1});var a=(0,i.useRef)(0),s=(0,o.Z)(),c=(0,i.useState)(r),l=c[0],u=c[1],d=(0,i.useCallback)((function(){for(var t=[],r=0;r<arguments.length;r++)t[r]=arguments[r];var i=++a.current;return l.loading||u((function(e){return(0,n.pi)((0,n.pi)({},e),{loading:!0})})),e.apply(void 0,t).then((function(e){return s()&&i===a.current&&u({value:e,loading:!1}),e}),(function(e){return s()&&i===a.current&&u({error:e,loading:!1}),e}))}),t);return[l,d]}}},function(e){e.O(0,[774,888,179],(function(){return t=75702,e(e.s=t);var t}));var t=e.O();_N_E=t}]);