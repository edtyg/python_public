"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[43],{96540:function(e,t,o){var n=o(95318);t.Z=void 0;var r=n(o(61268)),l=o(85893),a=(0,r.default)((0,l.jsx)("path",{d:"M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"}),"Add");t.Z=a},46901:function(e,t,o){o.d(t,{Z:function(){return W}});var n=o(63366),r=o(87462),l=o(67294),a=o(86010),i=o(27192),c=o(41796),s=o(11496),d=o(71657),u=o(98216),p=o(55113),m=o(28979);function k(e){return(0,m.Z)("MuiAlert",e)}var h,f=(0,o(76087).Z)("MuiAlert",["root","action","icon","message","filled","filledSuccess","filledInfo","filledWarning","filledError","outlined","outlinedSuccess","outlinedInfo","outlinedWarning","outlinedError","standard","standardSuccess","standardInfo","standardWarning","standardError"]),g=o(93946),y=o(82066),v=o(85893),L=(0,y.Z)((0,v.jsx)("path",{d:"M20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4C12.76,4 13.5,4.11 14.2, 4.31L15.77,2.74C14.61,2.26 13.34,2 12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0, 0 22,12M7.91,10.08L6.5,11.5L11,16L21,6L19.59,4.58L11,13.17L7.91,10.08Z"}),"SuccessOutlined"),b=(0,y.Z)((0,v.jsx)("path",{d:"M12 5.99L19.53 19H4.47L12 5.99M12 2L1 21h22L12 2zm1 14h-2v2h2v-2zm0-6h-2v4h2v-4z"}),"ReportProblemOutlined"),Z=(0,y.Z)((0,v.jsx)("path",{d:"M11 15h2v2h-2zm0-8h2v6h-2zm.99-5C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"}),"ErrorOutline"),x=(0,y.Z)((0,v.jsx)("path",{d:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20, 12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10, 10 0 0,0 12,2M11,17H13V11H11V17Z"}),"InfoOutlined"),C=o(34484);const E=["action","children","className","closeText","color","icon","iconMapping","onClose","role","severity","variant"],$=(0,s.ZP)(p.Z,{name:"MuiAlert",slot:"Root",overridesResolver:(e,t)=>{const{ownerState:o}=e;return[t.root,t[o.variant],t[`${o.variant}${(0,u.Z)(o.color||o.severity)}`]]}})((({theme:e,ownerState:t})=>{const o="light"===e.palette.mode?c._j:c.$n,n="light"===e.palette.mode?c.$n:c._j,l=t.color||t.severity;return(0,r.Z)({},e.typography.body2,{backgroundColor:"transparent",display:"flex",padding:"6px 16px"},l&&"standard"===t.variant&&{color:o(e.palette[l].light,.6),backgroundColor:n(e.palette[l].light,.9),[`& .${f.icon}`]:{color:"dark"===e.palette.mode?e.palette[l].main:e.palette[l].light}},l&&"outlined"===t.variant&&{color:o(e.palette[l].light,.6),border:`1px solid ${e.palette[l].light}`,[`& .${f.icon}`]:{color:"dark"===e.palette.mode?e.palette[l].main:e.palette[l].light}},l&&"filled"===t.variant&&{color:"#fff",fontWeight:e.typography.fontWeightMedium,backgroundColor:"dark"===e.palette.mode?e.palette[l].dark:e.palette[l].main})})),j=(0,s.ZP)("div",{name:"MuiAlert",slot:"Icon",overridesResolver:(e,t)=>t.icon})({marginRight:12,padding:"7px 0",display:"flex",fontSize:22,opacity:.9}),S=(0,s.ZP)("div",{name:"MuiAlert",slot:"Message",overridesResolver:(e,t)=>t.message})({padding:"8px 0"}),M=(0,s.ZP)("div",{name:"MuiAlert",slot:"Action",overridesResolver:(e,t)=>t.action})({display:"flex",alignItems:"flex-start",padding:"4px 0 0 16px",marginLeft:"auto",marginRight:-8}),w={success:(0,v.jsx)(L,{fontSize:"inherit"}),warning:(0,v.jsx)(b,{fontSize:"inherit"}),error:(0,v.jsx)(Z,{fontSize:"inherit"}),info:(0,v.jsx)(x,{fontSize:"inherit"})};var W=l.forwardRef((function(e,t){const o=(0,d.Z)({props:e,name:"MuiAlert"}),{action:l,children:c,className:s,closeText:p="Close",color:m,icon:f,iconMapping:y=w,onClose:L,role:b="alert",severity:Z="success",variant:x="standard"}=o,W=(0,n.Z)(o,E),V=(0,r.Z)({},o,{color:m,severity:Z,variant:x}),z=(e=>{const{variant:t,color:o,severity:n,classes:r}=e,l={root:["root",`${t}${(0,u.Z)(o||n)}`,`${t}`],icon:["icon"],message:["message"],action:["action"]};return(0,i.Z)(l,k,r)})(V);return(0,v.jsxs)($,(0,r.Z)({role:b,elevation:0,ownerState:V,className:(0,a.default)(z.root,s),ref:t},W,{children:[!1!==f?(0,v.jsx)(j,{ownerState:V,className:z.icon,children:f||y[Z]||w[Z]}):null,(0,v.jsx)(S,{ownerState:V,className:z.message,children:c}),null!=l?(0,v.jsx)(M,{className:z.action,children:l}):null,null==l&&L?(0,v.jsx)(M,{ownerState:V,className:z.action,children:(0,v.jsx)(g.Z,{size:"small","aria-label":p,title:p,color:"inherit",onClick:L,children:h||(h=(0,v.jsx)(C.Z,{fontSize:"small"}))})}):null]}))}))},87918:function(e,t,o){o.d(t,{Z:function(){return C}});var n=o(63366),r=o(87462),l=o(67294),a=o(86010),i=o(27192),c=o(41796),s=o(82066),d=o(85893),u=(0,s.Z)((0,d.jsx)("path",{d:"M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"}),"Cancel"),p=o(51705),m=o(98216),k=o(47739),h=o(71657),f=o(11496),g=o(28979);function y(e){return(0,g.Z)("MuiChip",e)}var v=(0,o(76087).Z)("MuiChip",["root","sizeSmall","sizeMedium","colorPrimary","colorSecondary","disabled","clickable","clickableColorPrimary","clickableColorSecondary","deletable","deletableColorPrimary","deletableColorSecondary","outlined","filled","outlinedPrimary","outlinedSecondary","avatar","avatarSmall","avatarMedium","avatarColorPrimary","avatarColorSecondary","icon","iconSmall","iconMedium","iconColorPrimary","iconColorSecondary","label","labelSmall","labelMedium","deleteIcon","deleteIconSmall","deleteIconMedium","deleteIconColorPrimary","deleteIconColorSecondary","deleteIconOutlinedColorPrimary","deleteIconOutlinedColorSecondary","focusVisible"]);const L=["avatar","className","clickable","color","component","deleteIcon","disabled","icon","label","onClick","onDelete","onKeyDown","onKeyUp","size","variant"],b=(0,f.ZP)("div",{name:"MuiChip",slot:"Root",overridesResolver:(e,t)=>{const{ownerState:o}=e,{color:n,clickable:r,onDelete:l,size:a,variant:i}=o;return[{[`& .${v.avatar}`]:t.avatar},{[`& .${v.avatar}`]:t[`avatar${(0,m.Z)(a)}`]},{[`& .${v.avatar}`]:t[`avatarColor${(0,m.Z)(n)}`]},{[`& .${v.icon}`]:t.icon},{[`& .${v.icon}`]:t[`icon${(0,m.Z)(a)}`]},{[`& .${v.icon}`]:t[`iconColor${(0,m.Z)(n)}`]},{[`& .${v.deleteIcon}`]:t.deleteIcon},{[`& .${v.deleteIcon}`]:t[`deleteIcon${(0,m.Z)(a)}`]},{[`& .${v.deleteIcon}`]:t[`deleteIconColor${(0,m.Z)(n)}`]},{[`& .${v.deleteIcon}`]:t[`deleteIconOutlinedColor${(0,m.Z)(n)}`]},t.root,t[`size${(0,m.Z)(a)}`],t[`color${(0,m.Z)(n)}`],r&&t.clickable,r&&"default"!==n&&t[`clickableColor${(0,m.Z)(n)})`],l&&t.deletable,l&&"default"!==n&&t[`deletableColor${(0,m.Z)(n)}`],t[i],"outlined"===i&&t[`outlined${(0,m.Z)(n)}`]]}})((({theme:e,ownerState:t})=>{const o=(0,c.Fq)(e.palette.text.primary,.26);return(0,r.Z)({maxWidth:"100%",fontFamily:e.typography.fontFamily,fontSize:e.typography.pxToRem(13),display:"inline-flex",alignItems:"center",justifyContent:"center",height:32,color:e.palette.text.primary,backgroundColor:e.palette.action.selected,borderRadius:16,whiteSpace:"nowrap",transition:e.transitions.create(["background-color","box-shadow"]),cursor:"default",outline:0,textDecoration:"none",border:0,padding:0,verticalAlign:"middle",boxSizing:"border-box",[`&.${v.disabled}`]:{opacity:e.palette.action.disabledOpacity,pointerEvents:"none"},[`& .${v.avatar}`]:{marginLeft:5,marginRight:-6,width:24,height:24,color:"light"===e.palette.mode?e.palette.grey[700]:e.palette.grey[300],fontSize:e.typography.pxToRem(12)},[`& .${v.avatarColorPrimary}`]:{color:e.palette.primary.contrastText,backgroundColor:e.palette.primary.dark},[`& .${v.avatarColorSecondary}`]:{color:e.palette.secondary.contrastText,backgroundColor:e.palette.secondary.dark},[`& .${v.avatarSmall}`]:{marginLeft:4,marginRight:-4,width:18,height:18,fontSize:e.typography.pxToRem(10)},[`& .${v.icon}`]:(0,r.Z)({color:"light"===e.palette.mode?e.palette.grey[700]:e.palette.grey[300],marginLeft:5,marginRight:-6},"small"===t.size&&{fontSize:18,marginLeft:4,marginRight:-4},"default"!==t.color&&{color:"inherit"}),[`& .${v.deleteIcon}`]:(0,r.Z)({WebkitTapHighlightColor:"transparent",color:o,fontSize:22,cursor:"pointer",margin:"0 5px 0 -6px","&:hover":{color:(0,c.Fq)(o,.4)}},"small"===t.size&&{fontSize:16,marginRight:4,marginLeft:-4},"default"!==t.color&&{color:(0,c.Fq)(e.palette[t.color].contrastText,.7),"&:hover, &:active":{color:e.palette[t.color].contrastText}})},"small"===t.size&&{height:24},"default"!==t.color&&{backgroundColor:e.palette[t.color].main,color:e.palette[t.color].contrastText},t.onDelete&&{[`&.${v.focusVisible}`]:{backgroundColor:(0,c.Fq)(e.palette.action.selected,e.palette.action.selectedOpacity+e.palette.action.focusOpacity)}},t.onDelete&&"default"!==t.color&&{[`&.${v.focusVisible}`]:{backgroundColor:e.palette[t.color].dark}})}),(({theme:e,ownerState:t})=>(0,r.Z)({},t.clickable&&{userSelect:"none",WebkitTapHighlightColor:"transparent",cursor:"pointer","&:hover":{backgroundColor:(0,c.Fq)(e.palette.action.selected,e.palette.action.selectedOpacity+e.palette.action.hoverOpacity)},[`&.${v.focusVisible}`]:{backgroundColor:(0,c.Fq)(e.palette.action.selected,e.palette.action.selectedOpacity+e.palette.action.focusOpacity)},"&:active":{boxShadow:e.shadows[1]}},t.clickable&&"default"!==t.color&&{[`&:hover, &.${v.focusVisible}`]:{backgroundColor:e.palette[t.color].dark}})),(({theme:e,ownerState:t})=>(0,r.Z)({},"outlined"===t.variant&&{backgroundColor:"transparent",border:`1px solid ${"light"===e.palette.mode?e.palette.grey[400]:e.palette.grey[700]}`,[`&.${v.clickable}:hover`]:{backgroundColor:e.palette.action.hover},[`&.${v.focusVisible}`]:{backgroundColor:e.palette.action.focus},[`& .${v.avatar}`]:{marginLeft:4},[`& .${v.avatarSmall}`]:{marginLeft:2},[`& .${v.icon}`]:{marginLeft:4},[`& .${v.iconSmall}`]:{marginLeft:2},[`& .${v.deleteIcon}`]:{marginRight:5},[`& .${v.deleteIconSmall}`]:{marginRight:3}},"outlined"===t.variant&&"default"!==t.color&&{color:e.palette[t.color].main,border:`1px solid ${(0,c.Fq)(e.palette[t.color].main,.7)}`,[`&.${v.clickable}:hover`]:{backgroundColor:(0,c.Fq)(e.palette[t.color].main,e.palette.action.hoverOpacity)},[`&.${v.focusVisible}`]:{backgroundColor:(0,c.Fq)(e.palette[t.color].main,e.palette.action.focusOpacity)},[`& .${v.deleteIcon}`]:{color:(0,c.Fq)(e.palette[t.color].main,.7),"&:hover, &:active":{color:e.palette[t.color].main}}}))),Z=(0,f.ZP)("span",{name:"MuiChip",slot:"Label",overridesResolver:(e,t)=>{const{ownerState:o}=e,{size:n}=o;return[t.label,t[`label${(0,m.Z)(n)}`]]}})((({ownerState:e})=>(0,r.Z)({overflow:"hidden",textOverflow:"ellipsis",paddingLeft:12,paddingRight:12,whiteSpace:"nowrap"},"small"===e.size&&{paddingLeft:8,paddingRight:8})));function x(e){return"Backspace"===e.key||"Delete"===e.key}var C=l.forwardRef((function(e,t){const o=(0,h.Z)({props:e,name:"MuiChip"}),{avatar:c,className:s,clickable:f,color:g="default",component:v,deleteIcon:C,disabled:E=!1,icon:$,label:j,onClick:S,onDelete:M,onKeyDown:w,onKeyUp:W,size:V="medium",variant:z="filled"}=o,I=(0,n.Z)(o,L),R=l.useRef(null),A=(0,p.Z)(R,t),F=e=>{e.stopPropagation(),M&&M(e)},H=!(!1===f||!S)||f,N="small"===V,O=H||M?k.Z:v||"div",P=(0,r.Z)({},o,{component:O,disabled:E,size:V,color:g,onDelete:!!M,clickable:H,variant:z}),T=(e=>{const{classes:t,disabled:o,size:n,color:r,onDelete:l,clickable:a,variant:c}=e,s={root:["root",c,o&&"disabled",`size${(0,m.Z)(n)}`,`color${(0,m.Z)(r)}`,a&&"clickable",a&&`clickableColor${(0,m.Z)(r)}`,l&&"deletable",l&&`deletableColor${(0,m.Z)(r)}`,`${c}${(0,m.Z)(r)}`],label:["label",`label${(0,m.Z)(n)}`],avatar:["avatar",`avatar${(0,m.Z)(n)}`,`avatarColor${(0,m.Z)(r)}`],icon:["icon",`icon${(0,m.Z)(n)}`,`iconColor${(0,m.Z)(r)}`],deleteIcon:["deleteIcon",`deleteIcon${(0,m.Z)(n)}`,`deleteIconColor${(0,m.Z)(r)}`,`deleteIconOutlinedColor${(0,m.Z)(r)}`]};return(0,i.Z)(s,y,t)})(P),D=O===k.Z?(0,r.Z)({component:v||"div",focusVisibleClassName:T.focusVisible},M&&{disableRipple:!0}):{};let q=null;if(M){const e=(0,a.default)("default"!==g&&("outlined"===z?T[`deleteIconOutlinedColor${(0,m.Z)(g)}`]:T[`deleteIconColor${(0,m.Z)(g)}`]),N&&T.deleteIconSmall);q=C&&l.isValidElement(C)?l.cloneElement(C,{className:(0,a.default)(C.props.className,T.deleteIcon,e),onClick:F}):(0,d.jsx)(u,{className:(0,a.default)(T.deleteIcon,e),onClick:F})}let _=null;c&&l.isValidElement(c)&&(_=l.cloneElement(c,{className:(0,a.default)(T.avatar,c.props.className)}));let K=null;return $&&l.isValidElement($)&&(K=l.cloneElement($,{className:(0,a.default)(T.icon,$.props.className)})),(0,d.jsxs)(b,(0,r.Z)({as:O,className:(0,a.default)(T.root,s),disabled:!(!H||!E)||void 0,onClick:S,onKeyDown:e=>{e.currentTarget===e.target&&x(e)&&e.preventDefault(),w&&w(e)},onKeyUp:e=>{e.currentTarget===e.target&&(M&&x(e)?M(e):"Escape"===e.key&&R.current&&R.current.blur()),W&&W(e)},ref:A,ownerState:P},D,I,{children:[_||K,(0,d.jsx)(Z,{className:(0,a.default)(T.label),ownerState:P,children:j}),q]}))}))},34484:function(e,t,o){o(67294);var n=o(82066),r=o(85893);t.Z=(0,n.Z)((0,r.jsx)("path",{d:"M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"}),"Close")},34800:function(e,t,o){var n=o(67294),r=o(19818),l=o(77258),a=new Map;a.set("bold",(function(e){return n.createElement(n.Fragment,null,n.createElement("polyline",{points:"168 168 216 168 216 40 88 40 88 88",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"24"}),n.createElement("rect",{x:"40",y:"88",width:"128",height:"128",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"24"}))})),a.set("duotone",(function(e){return n.createElement(n.Fragment,null,n.createElement("polygon",{points:"168 88 168 168 216 168 216 40 88 40 88 88 168 88",opacity:"0.2"}),n.createElement("polyline",{points:"168 168 216 168 216 40 88 40 88 88",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}),n.createElement("rect",{x:"40",y:"88",width:"128",height:"128",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}))})),a.set("fill",(function(){return n.createElement(n.Fragment,null,n.createElement("path",{d:"M216,32H88a8,8,0,0,0-8,8V80H40a8,8,0,0,0-8,8V216a8,8,0,0,0,8,8H168a8,8,0,0,0,8-8V176h40a8,8,0,0,0,8-8V40A8,8,0,0,0,216,32Zm-8,128H176V88a8,8,0,0,0-8-8H96V48H208Z"}))})),a.set("light",(function(e){return n.createElement(n.Fragment,null,n.createElement("polyline",{points:"168 168 216 168 216 40 88 40 88 88",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"12"}),n.createElement("rect",{x:"40",y:"88",width:"128",height:"128",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"12"}))})),a.set("thin",(function(e){return n.createElement(n.Fragment,null,n.createElement("polyline",{points:"168 168 216 168 216 40 88 40 88 88",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"8"}),n.createElement("rect",{x:"40",y:"88",width:"128",height:"128",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"8"}))})),a.set("regular",(function(e){return n.createElement(n.Fragment,null,n.createElement("polyline",{points:"168 168 216 168 216 40 88 40 88 88",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}),n.createElement("rect",{x:"40",y:"88",width:"128",height:"128",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}))}));var i=function(e,t){return(0,r._)(e,t,a)},c=(0,n.forwardRef)((function(e,t){return n.createElement(l.Z,Object.assign({ref:t},e,{renderPath:i}))}));c.displayName="Copy",t.Z=c},86286:function(e,t,o){var n=o(67294),r=o(19818),l=o(77258),a=new Map;a.set("bold",(function(e){return n.createElement(n.Fragment,null,n.createElement("path",{d:"M92.7,216H48a8,8,0,0,1-8-8V163.3a7.9,7.9,0,0,1,2.3-5.6l120-120a8,8,0,0,1,11.4,0l44.6,44.6a8,8,0,0,1,0,11.4l-120,120A7.9,7.9,0,0,1,92.7,216Z",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"24"}),n.createElement("line",{x1:"136",y1:"64",x2:"192",y2:"120",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"24"}))})),a.set("duotone",(function(e){return n.createElement(n.Fragment,null,n.createElement("path",{d:"M136,64l56,56,26.3-26.3a8,8,0,0,0,0-11.4L173.7,37.7a8,8,0,0,0-11.4,0Z",opacity:"0.2"}),n.createElement("line",{x1:"136",y1:"64",x2:"192",y2:"120",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}),n.createElement("path",{d:"M92.7,216H48a8,8,0,0,1-8-8V163.3a7.9,7.9,0,0,1,2.3-5.6l120-120a8,8,0,0,1,11.4,0l44.6,44.6a8,8,0,0,1,0,11.4l-120,120A7.9,7.9,0,0,1,92.7,216Z",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}))})),a.set("fill",(function(){return n.createElement(n.Fragment,null,n.createElement("path",{d:"M224,76.7,179.7,32.3a16.6,16.6,0,0,0-11.3-5A16,16,0,0,0,156.7,32L130.3,58.3h0L36.7,152A15.9,15.9,0,0,0,32,163.3V208a16,16,0,0,0,16,16H92.7a16.1,16.1,0,0,0,11.3-4.7l120-120A16.1,16.1,0,0,0,224,76.7Zm-32,32L147.3,64,168,43.3,212.7,88Z"}))})),a.set("light",(function(e){return n.createElement(n.Fragment,null,n.createElement("path",{d:"M92.7,216H48a8,8,0,0,1-8-8V163.3a7.9,7.9,0,0,1,2.3-5.6l120-120a8,8,0,0,1,11.4,0l44.6,44.6a8,8,0,0,1,0,11.4l-120,120A7.9,7.9,0,0,1,92.7,216Z",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"12"}),n.createElement("line",{x1:"136",y1:"64",x2:"192",y2:"120",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"12"}))})),a.set("thin",(function(e){return n.createElement(n.Fragment,null,n.createElement("path",{d:"M92.7,216H48a8,8,0,0,1-8-8V163.3a7.9,7.9,0,0,1,2.3-5.6l120-120a8,8,0,0,1,11.4,0l44.6,44.6a8,8,0,0,1,0,11.4l-120,120A7.9,7.9,0,0,1,92.7,216Z",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"8"}),n.createElement("line",{x1:"136",y1:"64",x2:"192",y2:"120",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"8"}))})),a.set("regular",(function(e){return n.createElement(n.Fragment,null,n.createElement("path",{d:"M92.7,216H48a8,8,0,0,1-8-8V163.3a7.9,7.9,0,0,1,2.3-5.6l120-120a8,8,0,0,1,11.4,0l44.6,44.6a8,8,0,0,1,0,11.4l-120,120A7.9,7.9,0,0,1,92.7,216Z",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}),n.createElement("line",{x1:"136",y1:"64",x2:"192",y2:"120",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}))}));var i=function(e,t){return(0,r._)(e,t,a)},c=(0,n.forwardRef)((function(e,t){return n.createElement(l.Z,Object.assign({ref:t},e,{renderPath:i}))}));c.displayName="PencilSimple",t.Z=c},7551:function(e,t,o){var n=o(67294),r=o(19818),l=o(77258),a=new Map;a.set("bold",(function(e){return n.createElement(n.Fragment,null,n.createElement("line",{x1:"216",y1:"60",x2:"40",y2:"60",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"24"}),n.createElement("line",{x1:"88",y1:"20",x2:"168",y2:"20",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"24"}),n.createElement("path",{d:"M200,60V208a8,8,0,0,1-8,8H64a8,8,0,0,1-8-8V60",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"24"}))})),a.set("duotone",(function(e){return n.createElement(n.Fragment,null,n.createElement("path",{d:"M200,56V208a8,8,0,0,1-8,8H64a8,8,0,0,1-8-8V56Z",opacity:"0.2"}),n.createElement("line",{x1:"216",y1:"56",x2:"40",y2:"56",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}),n.createElement("line",{x1:"88",y1:"24",x2:"168",y2:"24",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}),n.createElement("path",{d:"M200,56V208a8,8,0,0,1-8,8H64a8,8,0,0,1-8-8V56",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}))})),a.set("fill",(function(){return n.createElement(n.Fragment,null,n.createElement("path",{d:"M224,56a8,8,0,0,1-8,8h-8V208a16,16,0,0,1-16,16H64a16,16,0,0,1-16-16V64H40a8,8,0,0,1,0-16H216A8,8,0,0,1,224,56ZM88,32h80a8,8,0,0,0,0-16H88a8,8,0,0,0,0,16Z"}))})),a.set("light",(function(e){return n.createElement(n.Fragment,null,n.createElement("line",{x1:"216",y1:"56",x2:"40",y2:"56",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"12"}),n.createElement("line",{x1:"88",y1:"24",x2:"168",y2:"24",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"12"}),n.createElement("path",{d:"M200,56V208a8,8,0,0,1-8,8H64a8,8,0,0,1-8-8V56",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"12"}))})),a.set("thin",(function(e){return n.createElement(n.Fragment,null,n.createElement("line",{x1:"216",y1:"56",x2:"40",y2:"56",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"8"}),n.createElement("line",{x1:"88",y1:"24",x2:"168",y2:"24",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"8"}),n.createElement("path",{d:"M200,56V208a8,8,0,0,1-8,8H64a8,8,0,0,1-8-8V56",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"8"}))})),a.set("regular",(function(e){return n.createElement(n.Fragment,null,n.createElement("line",{x1:"216",y1:"56",x2:"40",y2:"56",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}),n.createElement("line",{x1:"88",y1:"24",x2:"168",y2:"24",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}),n.createElement("path",{d:"M200,56V208a8,8,0,0,1-8,8H64a8,8,0,0,1-8-8V56",fill:"none",stroke:e,strokeLinecap:"round",strokeLinejoin:"round",strokeWidth:"16"}))}));var i=function(e,t){return(0,r._)(e,t,a)},c=(0,n.forwardRef)((function(e,t){return n.createElement(l.Z,Object.assign({ref:t},e,{renderPath:i}))}));c.displayName="TrashSimple",t.Z=c}}]);