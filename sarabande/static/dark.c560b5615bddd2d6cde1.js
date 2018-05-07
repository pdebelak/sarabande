/*!
 * Copyright 2018 Peter Debelak
 * 
 * Sarabande is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * Sarabande is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with Sarabande.  If not, see <http://www.gnu.org/licenses/>.
 */!function(e){var t={};function n(o){if(t[o])return t[o].exports;var r=t[o]={i:o,l:!1,exports:{}};return e[o].call(r.exports,r,r.exports,n),r.l=!0,r.exports}n.m=e,n.c=t,n.d=function(e,t,o){n.o(e,t)||Object.defineProperty(e,t,{configurable:!1,enumerable:!0,get:o})},n.r=function(e){Object.defineProperty(e,"__esModule",{value:!0})},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="/",n(n.s=3)}({0:function(e,t,n){"use strict";n(13);function o(e){const t=document.createElement("span");t.className="close-button "+e.className,t.addEventListener("click",function(){const e=t.parentNode;e.parentNode.removeChild(e)}),e.parentNode.replaceChild(t,e)}document.querySelectorAll("[data-close-button]").forEach(o)},13:function(e,t){},3:function(e,t,n){"use strict";n.r(t);n(0),n(6)},6:function(e,t){}});