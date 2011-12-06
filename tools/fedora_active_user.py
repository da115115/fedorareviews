<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='en' lang='en'>
<head>
<title>fedora-misc.git - [no description]</title>
<meta name='generator' content='cgit v0.9.0.2'/>
<meta name='robots' content='index, nofollow'/>
<link rel='stylesheet' type='text/css' href='/cgit-data/cgit.css'/>
<link rel='alternate' title='Atom feed' href='http://ambre.pingoured.fr/cgit/fedora-misc.git/atom/fedora_active_user.py?h=master' type='application/atom+xml'/>
</head>
<body>
<div id='cgit'><table id='header'>
<tr>
<td class='logo' rowspan='2'><a href='/cgit/'><img src='/cgit-data/cgit.png' alt='cgit logo'/></a></td>
<td class='main'><a href='/cgit/'>index</a> : <a title='fedora-misc.git' href='/cgit/fedora-misc.git/'>fedora-misc.git</a></td><td class='form'><form method='get' action=''>
<select name='h' onchange='this.form.submit();'>
<option value='master' selected='selected'>master</option>
</select> <input type='submit' name='' value='switch'/></form></td></tr>
<tr><td class='sub'>[no description]</td><td class='sub right'>git repository hosting</td></tr></table>
<table class='tabs'><tr><td>
<a href='/cgit/fedora-misc.git/'>summary</a><a href='/cgit/fedora-misc.git/refs/'>refs</a><a href='/cgit/fedora-misc.git/log/fedora_active_user.py'>log</a><a class='active' href='/cgit/fedora-misc.git/tree/fedora_active_user.py'>tree</a><a href='/cgit/fedora-misc.git/commit/fedora_active_user.py'>commit</a><a href='/cgit/fedora-misc.git/diff/fedora_active_user.py'>diff</a><a href='/cgit/fedora-misc.git/stats/fedora_active_user.py'>stats</a></td><td class='form'><form class='right' method='get' action='/cgit/fedora-misc.git/log/fedora_active_user.py'>
<select name='qt'>
<option value='grep'>log msg</option>
<option value='author'>author</option>
<option value='committer'>committer</option>
<option value='range'>range</option>
</select>
<input class='txt' type='text' size='10' name='q' value=''/>
<input type='submit' value='search'/>
</form>
</td></tr></table>
<div class='path'>path: <a href='/cgit/fedora-misc.git/tree/'>root</a>/<a href='/cgit/fedora-misc.git/tree/fedora_active_user.py'>fedora_active_user.py</a></div><div class='content'>blob: 996657f9e37974b5b894490812c01011ceef4de6 (<a href='/cgit/fedora-misc.git/plain/fedora_active_user.py'>plain</a>)
<table summary='blob content' class='blob'>
<tr><td class='linenumbers'><pre><a class='no' id='n1' name='n1' href='#n1'>1</a>
<a class='no' id='n2' name='n2' href='#n2'>2</a>
<a class='no' id='n3' name='n3' href='#n3'>3</a>
<a class='no' id='n4' name='n4' href='#n4'>4</a>
<a class='no' id='n5' name='n5' href='#n5'>5</a>
<a class='no' id='n6' name='n6' href='#n6'>6</a>
<a class='no' id='n7' name='n7' href='#n7'>7</a>
<a class='no' id='n8' name='n8' href='#n8'>8</a>
<a class='no' id='n9' name='n9' href='#n9'>9</a>
<a class='no' id='n10' name='n10' href='#n10'>10</a>
<a class='no' id='n11' name='n11' href='#n11'>11</a>
<a class='no' id='n12' name='n12' href='#n12'>12</a>
<a class='no' id='n13' name='n13' href='#n13'>13</a>
<a class='no' id='n14' name='n14' href='#n14'>14</a>
<a class='no' id='n15' name='n15' href='#n15'>15</a>
<a class='no' id='n16' name='n16' href='#n16'>16</a>
<a class='no' id='n17' name='n17' href='#n17'>17</a>
<a class='no' id='n18' name='n18' href='#n18'>18</a>
<a class='no' id='n19' name='n19' href='#n19'>19</a>
<a class='no' id='n20' name='n20' href='#n20'>20</a>
<a class='no' id='n21' name='n21' href='#n21'>21</a>
<a class='no' id='n22' name='n22' href='#n22'>22</a>
<a class='no' id='n23' name='n23' href='#n23'>23</a>
<a class='no' id='n24' name='n24' href='#n24'>24</a>
<a class='no' id='n25' name='n25' href='#n25'>25</a>
<a class='no' id='n26' name='n26' href='#n26'>26</a>
<a class='no' id='n27' name='n27' href='#n27'>27</a>
<a class='no' id='n28' name='n28' href='#n28'>28</a>
<a class='no' id='n29' name='n29' href='#n29'>29</a>
<a class='no' id='n30' name='n30' href='#n30'>30</a>
<a class='no' id='n31' name='n31' href='#n31'>31</a>
<a class='no' id='n32' name='n32' href='#n32'>32</a>
<a class='no' id='n33' name='n33' href='#n33'>33</a>
<a class='no' id='n34' name='n34' href='#n34'>34</a>
<a class='no' id='n35' name='n35' href='#n35'>35</a>
<a class='no' id='n36' name='n36' href='#n36'>36</a>
<a class='no' id='n37' name='n37' href='#n37'>37</a>
<a class='no' id='n38' name='n38' href='#n38'>38</a>
<a class='no' id='n39' name='n39' href='#n39'>39</a>
<a class='no' id='n40' name='n40' href='#n40'>40</a>
<a class='no' id='n41' name='n41' href='#n41'>41</a>
<a class='no' id='n42' name='n42' href='#n42'>42</a>
<a class='no' id='n43' name='n43' href='#n43'>43</a>
<a class='no' id='n44' name='n44' href='#n44'>44</a>
<a class='no' id='n45' name='n45' href='#n45'>45</a>
<a class='no' id='n46' name='n46' href='#n46'>46</a>
<a class='no' id='n47' name='n47' href='#n47'>47</a>
<a class='no' id='n48' name='n48' href='#n48'>48</a>
<a class='no' id='n49' name='n49' href='#n49'>49</a>
<a class='no' id='n50' name='n50' href='#n50'>50</a>
<a class='no' id='n51' name='n51' href='#n51'>51</a>
<a class='no' id='n52' name='n52' href='#n52'>52</a>
<a class='no' id='n53' name='n53' href='#n53'>53</a>
<a class='no' id='n54' name='n54' href='#n54'>54</a>
<a class='no' id='n55' name='n55' href='#n55'>55</a>
<a class='no' id='n56' name='n56' href='#n56'>56</a>
<a class='no' id='n57' name='n57' href='#n57'>57</a>
<a class='no' id='n58' name='n58' href='#n58'>58</a>
<a class='no' id='n59' name='n59' href='#n59'>59</a>
<a class='no' id='n60' name='n60' href='#n60'>60</a>
<a class='no' id='n61' name='n61' href='#n61'>61</a>
<a class='no' id='n62' name='n62' href='#n62'>62</a>
<a class='no' id='n63' name='n63' href='#n63'>63</a>
<a class='no' id='n64' name='n64' href='#n64'>64</a>
<a class='no' id='n65' name='n65' href='#n65'>65</a>
<a class='no' id='n66' name='n66' href='#n66'>66</a>
<a class='no' id='n67' name='n67' href='#n67'>67</a>
<a class='no' id='n68' name='n68' href='#n68'>68</a>
<a class='no' id='n69' name='n69' href='#n69'>69</a>
<a class='no' id='n70' name='n70' href='#n70'>70</a>
<a class='no' id='n71' name='n71' href='#n71'>71</a>
<a class='no' id='n72' name='n72' href='#n72'>72</a>
<a class='no' id='n73' name='n73' href='#n73'>73</a>
<a class='no' id='n74' name='n74' href='#n74'>74</a>
<a class='no' id='n75' name='n75' href='#n75'>75</a>
<a class='no' id='n76' name='n76' href='#n76'>76</a>
<a class='no' id='n77' name='n77' href='#n77'>77</a>
<a class='no' id='n78' name='n78' href='#n78'>78</a>
<a class='no' id='n79' name='n79' href='#n79'>79</a>
<a class='no' id='n80' name='n80' href='#n80'>80</a>
<a class='no' id='n81' name='n81' href='#n81'>81</a>
<a class='no' id='n82' name='n82' href='#n82'>82</a>
<a class='no' id='n83' name='n83' href='#n83'>83</a>
<a class='no' id='n84' name='n84' href='#n84'>84</a>
<a class='no' id='n85' name='n85' href='#n85'>85</a>
<a class='no' id='n86' name='n86' href='#n86'>86</a>
<a class='no' id='n87' name='n87' href='#n87'>87</a>
<a class='no' id='n88' name='n88' href='#n88'>88</a>
<a class='no' id='n89' name='n89' href='#n89'>89</a>
<a class='no' id='n90' name='n90' href='#n90'>90</a>
<a class='no' id='n91' name='n91' href='#n91'>91</a>
<a class='no' id='n92' name='n92' href='#n92'>92</a>
<a class='no' id='n93' name='n93' href='#n93'>93</a>
<a class='no' id='n94' name='n94' href='#n94'>94</a>
<a class='no' id='n95' name='n95' href='#n95'>95</a>
<a class='no' id='n96' name='n96' href='#n96'>96</a>
<a class='no' id='n97' name='n97' href='#n97'>97</a>
<a class='no' id='n98' name='n98' href='#n98'>98</a>
<a class='no' id='n99' name='n99' href='#n99'>99</a>
<a class='no' id='n100' name='n100' href='#n100'>100</a>
<a class='no' id='n101' name='n101' href='#n101'>101</a>
<a class='no' id='n102' name='n102' href='#n102'>102</a>
<a class='no' id='n103' name='n103' href='#n103'>103</a>
<a class='no' id='n104' name='n104' href='#n104'>104</a>
<a class='no' id='n105' name='n105' href='#n105'>105</a>
<a class='no' id='n106' name='n106' href='#n106'>106</a>
<a class='no' id='n107' name='n107' href='#n107'>107</a>
<a class='no' id='n108' name='n108' href='#n108'>108</a>
<a class='no' id='n109' name='n109' href='#n109'>109</a>
<a class='no' id='n110' name='n110' href='#n110'>110</a>
<a class='no' id='n111' name='n111' href='#n111'>111</a>
<a class='no' id='n112' name='n112' href='#n112'>112</a>
<a class='no' id='n113' name='n113' href='#n113'>113</a>
<a class='no' id='n114' name='n114' href='#n114'>114</a>
<a class='no' id='n115' name='n115' href='#n115'>115</a>
<a class='no' id='n116' name='n116' href='#n116'>116</a>
<a class='no' id='n117' name='n117' href='#n117'>117</a>
<a class='no' id='n118' name='n118' href='#n118'>118</a>
<a class='no' id='n119' name='n119' href='#n119'>119</a>
<a class='no' id='n120' name='n120' href='#n120'>120</a>
<a class='no' id='n121' name='n121' href='#n121'>121</a>
<a class='no' id='n122' name='n122' href='#n122'>122</a>
<a class='no' id='n123' name='n123' href='#n123'>123</a>
<a class='no' id='n124' name='n124' href='#n124'>124</a>
<a class='no' id='n125' name='n125' href='#n125'>125</a>
<a class='no' id='n126' name='n126' href='#n126'>126</a>
<a class='no' id='n127' name='n127' href='#n127'>127</a>
<a class='no' id='n128' name='n128' href='#n128'>128</a>
<a class='no' id='n129' name='n129' href='#n129'>129</a>
<a class='no' id='n130' name='n130' href='#n130'>130</a>
<a class='no' id='n131' name='n131' href='#n131'>131</a>
<a class='no' id='n132' name='n132' href='#n132'>132</a>
<a class='no' id='n133' name='n133' href='#n133'>133</a>
<a class='no' id='n134' name='n134' href='#n134'>134</a>
<a class='no' id='n135' name='n135' href='#n135'>135</a>
<a class='no' id='n136' name='n136' href='#n136'>136</a>
<a class='no' id='n137' name='n137' href='#n137'>137</a>
<a class='no' id='n138' name='n138' href='#n138'>138</a>
<a class='no' id='n139' name='n139' href='#n139'>139</a>
<a class='no' id='n140' name='n140' href='#n140'>140</a>
<a class='no' id='n141' name='n141' href='#n141'>141</a>
<a class='no' id='n142' name='n142' href='#n142'>142</a>
<a class='no' id='n143' name='n143' href='#n143'>143</a>
<a class='no' id='n144' name='n144' href='#n144'>144</a>
<a class='no' id='n145' name='n145' href='#n145'>145</a>
<a class='no' id='n146' name='n146' href='#n146'>146</a>
<a class='no' id='n147' name='n147' href='#n147'>147</a>
<a class='no' id='n148' name='n148' href='#n148'>148</a>
<a class='no' id='n149' name='n149' href='#n149'>149</a>
<a class='no' id='n150' name='n150' href='#n150'>150</a>
<a class='no' id='n151' name='n151' href='#n151'>151</a>
<a class='no' id='n152' name='n152' href='#n152'>152</a>
<a class='no' id='n153' name='n153' href='#n153'>153</a>
<a class='no' id='n154' name='n154' href='#n154'>154</a>
<a class='no' id='n155' name='n155' href='#n155'>155</a>
<a class='no' id='n156' name='n156' href='#n156'>156</a>
<a class='no' id='n157' name='n157' href='#n157'>157</a>
<a class='no' id='n158' name='n158' href='#n158'>158</a>
<a class='no' id='n159' name='n159' href='#n159'>159</a>
<a class='no' id='n160' name='n160' href='#n160'>160</a>
<a class='no' id='n161' name='n161' href='#n161'>161</a>
<a class='no' id='n162' name='n162' href='#n162'>162</a>
<a class='no' id='n163' name='n163' href='#n163'>163</a>
<a class='no' id='n164' name='n164' href='#n164'>164</a>
<a class='no' id='n165' name='n165' href='#n165'>165</a>
<a class='no' id='n166' name='n166' href='#n166'>166</a>
<a class='no' id='n167' name='n167' href='#n167'>167</a>
<a class='no' id='n168' name='n168' href='#n168'>168</a>
<a class='no' id='n169' name='n169' href='#n169'>169</a>
<a class='no' id='n170' name='n170' href='#n170'>170</a>
<a class='no' id='n171' name='n171' href='#n171'>171</a>
<a class='no' id='n172' name='n172' href='#n172'>172</a>
<a class='no' id='n173' name='n173' href='#n173'>173</a>
<a class='no' id='n174' name='n174' href='#n174'>174</a>
<a class='no' id='n175' name='n175' href='#n175'>175</a>
<a class='no' id='n176' name='n176' href='#n176'>176</a>
<a class='no' id='n177' name='n177' href='#n177'>177</a>
<a class='no' id='n178' name='n178' href='#n178'>178</a>
<a class='no' id='n179' name='n179' href='#n179'>179</a>
<a class='no' id='n180' name='n180' href='#n180'>180</a>
<a class='no' id='n181' name='n181' href='#n181'>181</a>
<a class='no' id='n182' name='n182' href='#n182'>182</a>
<a class='no' id='n183' name='n183' href='#n183'>183</a>
<a class='no' id='n184' name='n184' href='#n184'>184</a>
<a class='no' id='n185' name='n185' href='#n185'>185</a>
<a class='no' id='n186' name='n186' href='#n186'>186</a>
<a class='no' id='n187' name='n187' href='#n187'>187</a>
<a class='no' id='n188' name='n188' href='#n188'>188</a>
<a class='no' id='n189' name='n189' href='#n189'>189</a>
<a class='no' id='n190' name='n190' href='#n190'>190</a>
<a class='no' id='n191' name='n191' href='#n191'>191</a>
<a class='no' id='n192' name='n192' href='#n192'>192</a>
<a class='no' id='n193' name='n193' href='#n193'>193</a>
<a class='no' id='n194' name='n194' href='#n194'>194</a>
<a class='no' id='n195' name='n195' href='#n195'>195</a>
<a class='no' id='n196' name='n196' href='#n196'>196</a>
<a class='no' id='n197' name='n197' href='#n197'>197</a>
<a class='no' id='n198' name='n198' href='#n198'>198</a>
<a class='no' id='n199' name='n199' href='#n199'>199</a>
<a class='no' id='n200' name='n200' href='#n200'>200</a>
<a class='no' id='n201' name='n201' href='#n201'>201</a>
<a class='no' id='n202' name='n202' href='#n202'>202</a>
<a class='no' id='n203' name='n203' href='#n203'>203</a>
<a class='no' id='n204' name='n204' href='#n204'>204</a>
<a class='no' id='n205' name='n205' href='#n205'>205</a>
<a class='no' id='n206' name='n206' href='#n206'>206</a>
<a class='no' id='n207' name='n207' href='#n207'>207</a>
<a class='no' id='n208' name='n208' href='#n208'>208</a>
<a class='no' id='n209' name='n209' href='#n209'>209</a>
<a class='no' id='n210' name='n210' href='#n210'>210</a>
<a class='no' id='n211' name='n211' href='#n211'>211</a>
<a class='no' id='n212' name='n212' href='#n212'>212</a>
<a class='no' id='n213' name='n213' href='#n213'>213</a>
<a class='no' id='n214' name='n214' href='#n214'>214</a>
<a class='no' id='n215' name='n215' href='#n215'>215</a>
<a class='no' id='n216' name='n216' href='#n216'>216</a>
<a class='no' id='n217' name='n217' href='#n217'>217</a>
<a class='no' id='n218' name='n218' href='#n218'>218</a>
<a class='no' id='n219' name='n219' href='#n219'>219</a>
<a class='no' id='n220' name='n220' href='#n220'>220</a>
<a class='no' id='n221' name='n221' href='#n221'>221</a>
<a class='no' id='n222' name='n222' href='#n222'>222</a>
<a class='no' id='n223' name='n223' href='#n223'>223</a>
<a class='no' id='n224' name='n224' href='#n224'>224</a>
<a class='no' id='n225' name='n225' href='#n225'>225</a>
<a class='no' id='n226' name='n226' href='#n226'>226</a>
<a class='no' id='n227' name='n227' href='#n227'>227</a>
<a class='no' id='n228' name='n228' href='#n228'>228</a>
<a class='no' id='n229' name='n229' href='#n229'>229</a>
<a class='no' id='n230' name='n230' href='#n230'>230</a>
<a class='no' id='n231' name='n231' href='#n231'>231</a>
<a class='no' id='n232' name='n232' href='#n232'>232</a>
<a class='no' id='n233' name='n233' href='#n233'>233</a>
<a class='no' id='n234' name='n234' href='#n234'>234</a>
<a class='no' id='n235' name='n235' href='#n235'>235</a>
<a class='no' id='n236' name='n236' href='#n236'>236</a>
<a class='no' id='n237' name='n237' href='#n237'>237</a>
<a class='no' id='n238' name='n238' href='#n238'>238</a>
<a class='no' id='n239' name='n239' href='#n239'>239</a>
<a class='no' id='n240' name='n240' href='#n240'>240</a>
<a class='no' id='n241' name='n241' href='#n241'>241</a>
<a class='no' id='n242' name='n242' href='#n242'>242</a>
<a class='no' id='n243' name='n243' href='#n243'>243</a>
<a class='no' id='n244' name='n244' href='#n244'>244</a>
<a class='no' id='n245' name='n245' href='#n245'>245</a>
<a class='no' id='n246' name='n246' href='#n246'>246</a>
<a class='no' id='n247' name='n247' href='#n247'>247</a>
<a class='no' id='n248' name='n248' href='#n248'>248</a>
<a class='no' id='n249' name='n249' href='#n249'>249</a>
<a class='no' id='n250' name='n250' href='#n250'>250</a>
<a class='no' id='n251' name='n251' href='#n251'>251</a>
<a class='no' id='n252' name='n252' href='#n252'>252</a>
<a class='no' id='n253' name='n253' href='#n253'>253</a>
<a class='no' id='n254' name='n254' href='#n254'>254</a>
<a class='no' id='n255' name='n255' href='#n255'>255</a>
<a class='no' id='n256' name='n256' href='#n256'>256</a>
<a class='no' id='n257' name='n257' href='#n257'>257</a>
<a class='no' id='n258' name='n258' href='#n258'>258</a>
<a class='no' id='n259' name='n259' href='#n259'>259</a>
<a class='no' id='n260' name='n260' href='#n260'>260</a>
<a class='no' id='n261' name='n261' href='#n261'>261</a>
<a class='no' id='n262' name='n262' href='#n262'>262</a>
<a class='no' id='n263' name='n263' href='#n263'>263</a>
<a class='no' id='n264' name='n264' href='#n264'>264</a>
<a class='no' id='n265' name='n265' href='#n265'>265</a>
<a class='no' id='n266' name='n266' href='#n266'>266</a>
<a class='no' id='n267' name='n267' href='#n267'>267</a>
<a class='no' id='n268' name='n268' href='#n268'>268</a>
<a class='no' id='n269' name='n269' href='#n269'>269</a>
<a class='no' id='n270' name='n270' href='#n270'>270</a>
<a class='no' id='n271' name='n271' href='#n271'>271</a>
<a class='no' id='n272' name='n272' href='#n272'>272</a>
<a class='no' id='n273' name='n273' href='#n273'>273</a>
<a class='no' id='n274' name='n274' href='#n274'>274</a>
<a class='no' id='n275' name='n275' href='#n275'>275</a>
<a class='no' id='n276' name='n276' href='#n276'>276</a>
<a class='no' id='n277' name='n277' href='#n277'>277</a>
<a class='no' id='n278' name='n278' href='#n278'>278</a>
<a class='no' id='n279' name='n279' href='#n279'>279</a>
<a class='no' id='n280' name='n280' href='#n280'>280</a>
<a class='no' id='n281' name='n281' href='#n281'>281</a>
<a class='no' id='n282' name='n282' href='#n282'>282</a>
<a class='no' id='n283' name='n283' href='#n283'>283</a>
<a class='no' id='n284' name='n284' href='#n284'>284</a>
<a class='no' id='n285' name='n285' href='#n285'>285</a>
<a class='no' id='n286' name='n286' href='#n286'>286</a>
<a class='no' id='n287' name='n287' href='#n287'>287</a>
<a class='no' id='n288' name='n288' href='#n288'>288</a>
<a class='no' id='n289' name='n289' href='#n289'>289</a>
<a class='no' id='n290' name='n290' href='#n290'>290</a>
<a class='no' id='n291' name='n291' href='#n291'>291</a>
<a class='no' id='n292' name='n292' href='#n292'>292</a>
<a class='no' id='n293' name='n293' href='#n293'>293</a>
<a class='no' id='n294' name='n294' href='#n294'>294</a>
<a class='no' id='n295' name='n295' href='#n295'>295</a>
<a class='no' id='n296' name='n296' href='#n296'>296</a>
<a class='no' id='n297' name='n297' href='#n297'>297</a>
<a class='no' id='n298' name='n298' href='#n298'>298</a>
<a class='no' id='n299' name='n299' href='#n299'>299</a>
<a class='no' id='n300' name='n300' href='#n300'>300</a>
<a class='no' id='n301' name='n301' href='#n301'>301</a>
<a class='no' id='n302' name='n302' href='#n302'>302</a>
<a class='no' id='n303' name='n303' href='#n303'>303</a>
<a class='no' id='n304' name='n304' href='#n304'>304</a>
<a class='no' id='n305' name='n305' href='#n305'>305</a>
<a class='no' id='n306' name='n306' href='#n306'>306</a>
<a class='no' id='n307' name='n307' href='#n307'>307</a>
<a class='no' id='n308' name='n308' href='#n308'>308</a>
<a class='no' id='n309' name='n309' href='#n309'>309</a>
<a class='no' id='n310' name='n310' href='#n310'>310</a>
<a class='no' id='n311' name='n311' href='#n311'>311</a>
<a class='no' id='n312' name='n312' href='#n312'>312</a>
<a class='no' id='n313' name='n313' href='#n313'>313</a>
<a class='no' id='n314' name='n314' href='#n314'>314</a>
<a class='no' id='n315' name='n315' href='#n315'>315</a>
<a class='no' id='n316' name='n316' href='#n316'>316</a>
<a class='no' id='n317' name='n317' href='#n317'>317</a>
<a class='no' id='n318' name='n318' href='#n318'>318</a>
<a class='no' id='n319' name='n319' href='#n319'>319</a>
<a class='no' id='n320' name='n320' href='#n320'>320</a>
<a class='no' id='n321' name='n321' href='#n321'>321</a>
<a class='no' id='n322' name='n322' href='#n322'>322</a>
<a class='no' id='n323' name='n323' href='#n323'>323</a>
<a class='no' id='n324' name='n324' href='#n324'>324</a>
<a class='no' id='n325' name='n325' href='#n325'>325</a>
<a class='no' id='n326' name='n326' href='#n326'>326</a>
<a class='no' id='n327' name='n327' href='#n327'>327</a>
<a class='no' id='n328' name='n328' href='#n328'>328</a>
<a class='no' id='n329' name='n329' href='#n329'>329</a>
<a class='no' id='n330' name='n330' href='#n330'>330</a>
<a class='no' id='n331' name='n331' href='#n331'>331</a>
<a class='no' id='n332' name='n332' href='#n332'>332</a>
<a class='no' id='n333' name='n333' href='#n333'>333</a>
<a class='no' id='n334' name='n334' href='#n334'>334</a>
<a class='no' id='n335' name='n335' href='#n335'>335</a>
<a class='no' id='n336' name='n336' href='#n336'>336</a>
<a class='no' id='n337' name='n337' href='#n337'>337</a>
<a class='no' id='n338' name='n338' href='#n338'>338</a>
<a class='no' id='n339' name='n339' href='#n339'>339</a>
<a class='no' id='n340' name='n340' href='#n340'>340</a>
<a class='no' id='n341' name='n341' href='#n341'>341</a>
<a class='no' id='n342' name='n342' href='#n342'>342</a>
<a class='no' id='n343' name='n343' href='#n343'>343</a>
<a class='no' id='n344' name='n344' href='#n344'>344</a>
<a class='no' id='n345' name='n345' href='#n345'>345</a>
<a class='no' id='n346' name='n346' href='#n346'>346</a>
<a class='no' id='n347' name='n347' href='#n347'>347</a>
<a class='no' id='n348' name='n348' href='#n348'>348</a>
<a class='no' id='n349' name='n349' href='#n349'>349</a>
<a class='no' id='n350' name='n350' href='#n350'>350</a>
<a class='no' id='n351' name='n351' href='#n351'>351</a>
<a class='no' id='n352' name='n352' href='#n352'>352</a>
<a class='no' id='n353' name='n353' href='#n353'>353</a>
<a class='no' id='n354' name='n354' href='#n354'>354</a>
<a class='no' id='n355' name='n355' href='#n355'>355</a>
<a class='no' id='n356' name='n356' href='#n356'>356</a>
<a class='no' id='n357' name='n357' href='#n357'>357</a>
<a class='no' id='n358' name='n358' href='#n358'>358</a>
<a class='no' id='n359' name='n359' href='#n359'>359</a>
<a class='no' id='n360' name='n360' href='#n360'>360</a>
<a class='no' id='n361' name='n361' href='#n361'>361</a>
<a class='no' id='n362' name='n362' href='#n362'>362</a>
<a class='no' id='n363' name='n363' href='#n363'>363</a>
<a class='no' id='n364' name='n364' href='#n364'>364</a>
<a class='no' id='n365' name='n365' href='#n365'>365</a>
<a class='no' id='n366' name='n366' href='#n366'>366</a>
<a class='no' id='n367' name='n367' href='#n367'>367</a>
<a class='no' id='n368' name='n368' href='#n368'>368</a>
<a class='no' id='n369' name='n369' href='#n369'>369</a>
<a class='no' id='n370' name='n370' href='#n370'>370</a>
<a class='no' id='n371' name='n371' href='#n371'>371</a>
<a class='no' id='n372' name='n372' href='#n372'>372</a>
<a class='no' id='n373' name='n373' href='#n373'>373</a>
<a class='no' id='n374' name='n374' href='#n374'>374</a>
<a class='no' id='n375' name='n375' href='#n375'>375</a>
<a class='no' id='n376' name='n376' href='#n376'>376</a>
<a class='no' id='n377' name='n377' href='#n377'>377</a>
<a class='no' id='n378' name='n378' href='#n378'>378</a>
<a class='no' id='n379' name='n379' href='#n379'>379</a>
<a class='no' id='n380' name='n380' href='#n380'>380</a>
<a class='no' id='n381' name='n381' href='#n381'>381</a>
<a class='no' id='n382' name='n382' href='#n382'>382</a>
<a class='no' id='n383' name='n383' href='#n383'>383</a>
<a class='no' id='n384' name='n384' href='#n384'>384</a>
</pre></td>
<td class='lines'><pre><code>#!/usr/bin/python -tt
#-*- coding: utf-8 -*-

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
This program performs a number of check to have an educated guess as to
whether someone can be consider as 'active' or not within the fedora
project.
"""

import argparse
import fedora_cert
import getpass
import koji
import logging
import re
import sys
import time
import urllib
from fedora.client import AppError, ServerError, AccountSystem
from bugzilla.rhbugzilla import RHBugzilla3


kojiclient = koji.ClientSession('http://koji.fedoraproject.org/kojihub',
                {})
fasclient = AccountSystem()
bzclient = RHBugzilla3(url='https://bugzilla.redhat.com/xmlrpc.cgi')


# Initial simple logging stuff
logging.basicConfig()
log = logging.getLogger("pkgdb")
if '--debug' in sys.argv:
    log.setLevel(logging.DEBUG)
    #pkgdbclient.debug = True
elif '--verbose' in sys.argv:
    log.setLevel(logging.INFO)


_table_keys = {
    'user_perms' : ['user_id', 'perm_id'],
    'user_groups' : ['user_id', 'group_id'],
    'tag_inheritance' : ['tag_id', 'parent_id'],
    'tag_config' : ['tag_id'],
    'build_target_config' : ['build_target_id'],
    'external_repo_config' : ['external_repo_id'],
    'tag_external_repos' : ['tag_id', 'external_repo_id'],
    'tag_listing' : ['build_id', 'tag_id'],
    'tag_packages' : ['package_id', 'tag_id'],
    'group_config' : ['group_id', 'tag_id'],
    'group_req_listing' : ['group_id', 'tag_id', 'req_id'],
    'group_package_listing' : ['group_id', 'tag_id', 'package'],
    }


_mailing_lists = [
    'gmane.linux.redhat.fedora.devel',
    'gmane.linux.redhat.fedora.artwork',
    'gmane.linux.redhat.fedora.desktop',
    'gmane.linux.redhat.fedora.epel.devel',
    'gmane.linux.redhat.fedora.extras.packaging',
    'gmane.linux.redhat.fedora.fonts',
    'gmane.linux.redhat.fedora.general',
    'gmane.linux.redhat.fedora.infrastructure',
    'gmane.linux.redhat.fedora.kde',
    'gmane.linux.redhat.fedora.perl'
    ]

def _get_bugzilla_history(email):
    """ Query the bugzilla for all bugs to which the provided email
    is either assigned or cc'ed. Then for each bug found, print the
    latest comment from this user (if any).

    :arg email, the email address used in the bugzilla and for which we
    are searching for activities.
    """
    bugbz = bzclient.query(
         {'emailtype1': 'substring',
         'emailcc1': True,
         'bug_status': ['ASSIGNED', 'NEW', 'NEEDINFO'],
         'email1': email})
    print "   {0} bugs assigned or cc to {1} ".format(len(bugbz), email)

    for bug in bugbz:
        string = None
        log.debug(bug.bug_id)
        buginfo = bzclient.getbug(bug.bug_id)
        for com in buginfo.longdescs:
            if com['author']['login_name'] == email:
                string = "  %s %s %s" %(bug.bug_id, com['time'],
                    com['author']['login_name'])
        if string:
            print string


def _get_koji_history(username):
    """
    Print the last operation made by this user in koji.
    This is partly stolen from the koji client written by:
       Dennis Gregorovic &lt;dgregor@redhat.com&gt;
       Mike McLean &lt;mikem@redhat.com&gt;
       Cristian Balint &lt;cbalint@redhat.com&gt;

    :arg username, the fas username whose history is investigated.
    """
    log.debug("Search last history element in koji for {0} ".format(username))
    histdata = kojiclient.queryHistory(user=username)
    timeline = []
    def distinguish_match(x, name):
        """determine if create or revoke event matched"""
        name = "_" + name
        ret = True
        for key in x:
            if key.startswith(name):
                ret = ret and x[key]
        return ret
    for table in histdata:
        hist = histdata[table]
        for x in hist:
            if x['revoke_event'] is not None:
                if distinguish_match(x, 'revoked'):
                    timeline.append((x['revoke_event'], table, 0, x.copy()))
                #pprint.pprint(timeline[-1])
            if distinguish_match(x, 'created'):
                timeline.append((x['create_event'], table, 1, x))
    timeline.sort()
    #group edits together
    new_timeline = []
    last_event = None
    edit_index = {}
    for entry in timeline:
        event_id, table, create, x = entry
        if event_id != last_event:
            edit_index = {}
            last_event = event_id
        key = tuple([x[k] for k in _table_keys[table]])
        prev = edit_index.get((table, event_id), {}).get(key)
        if prev:
            prev[-1].setdefault('.related', []).append(entry)
        else:
            edit_index.setdefault((table, event_id), {})[key] = entry
            new_timeline.append(entry)
    for entry in new_timeline[-1:]:
        _print_histline(entry)


def _get_last_email_list(email):
    """ Using gname, let's find the last email sent by this email.

    :arg email, the email address to search on the mailing lists.
    """
    for mailinglist in _mailing_lists:
        url = "http://search.gmane.org/?query=&amp;group=%s&amp;author=%s&amp;sort=date" \
            % (mailinglist, email)
        stream = urllib.urlopen(url)
        page = stream.read()
        stream.close()
        regex = re.compile(r'.*(\d\d\d\d-\d\d-\d\d).*')
        for line in page.split('\n'):
            if 'GMT' in line:
                g = regex.match(line)
                print '  ', g.groups()[0], mailinglist
                break


def _get_last_website_login(username):
    """ Retrieve from FAS the last time this user has been seen.

    :arg username, the fas username from who we would like to see the
        last connection in FAS.
    """
    try:
        fasusername = fedora_cert.read_user_cert()
    except:
        log.debug('Could not read Fedora cert, using login name')
        fasusername = raw_input('FAS username: ')
    password = getpass.getpass('   FAS password for %s: ' % fasusername)
    fasclient.username = fasusername
    fasclient.password = password
    person = fasclient.person_by_username(username)
    print '  ', username, person['last_seen']

def _print_histline(entry, **kwargs):
    """
    This is mainly stolen from the koji client written by:
       Dennis Gregorovic &lt;dgregor@redhat.com&gt;
       Mike McLean &lt;mikem@redhat.com&gt;
       Cristian Balint &lt;cbalint@redhat.com&gt;
    """
    event_id, table, create, x = entry
    who = None
    edit = x.get('.related')
    if edit:
        del x['.related']
        bad_edit = None
        if len(edit) != 1:
            bad_edit = "%i elements" % len(edit)+1
        other = edit[0]
        #check edit for sanity
        if create or not other[2]:
            bad_edit = "out of order"
        if event_id != other[0]:
            bad_edit = "non-matching"
        if bad_edit:
            print "Warning: unusual edit at event %i in table %s (%s)" % (event_id, table, bad_edit)
            #we'll simply treat them as separate events
            pprint.pprint(entry)
            pprint.pprint(edit)
            _print_histline(entry, **kwargs)
            for data in edit:
                _print_histline(entry, **kwargs)
            return
    if create:
        ts = x['create_ts']
        if x.has_key('creator_name'):
            who = "by %(creator_name)s"
    else:
        ts = x['revoke_ts']
        if x.has_key('revoker_name'):
            who = "by %(revoker_name)s"
    if table == 'tag_listing':
        if edit:
            fmt = "%(name)s-%(version)s-%(release)s re-tagged into %(tag.name)s"
        elif create:
            fmt = "%(name)s-%(version)s-%(release)s tagged into %(tag.name)s"
        else:
            fmt = "%(name)s-%(version)s-%(release)s untagged from %(tag.name)s"
    elif table == 'user_perms':
        if edit:
            fmt = "permission %(permission.name)s re-granted to %(user.name)s"
        elif create:
            fmt = "permission %(permission.name)s granted to %(user.name)s"
        else:
            fmt = "permission %(permission.name)s revoked for %(user.name)s"
    elif table == 'user_groups':
        if edit:
            fmt = "user %(user.name)s re-added to group %(group.name)s"
        elif create:
            fmt = "user %(user.name)s added to group %(group.name)s"
        else:
            fmt = "user %(user.name)s removed from group %(group.name)s"
    elif table == 'tag_packages':
        if edit:
            fmt = "package list entry for %(package.name)s in %(tag.name)s updated"
        elif create:
            fmt = "package list entry created: %(package.name)s in %(tag.name)s"
        else:
            fmt = "package list entry revoked: %(package.name)s in %(tag.name)s"
    elif table == 'tag_inheritance':
        if edit:
            fmt = "inheritance line %(tag.name)s-&gt;%(parent.name)s updated"
        elif create:
            fmt = "inheritance line %(tag.name)s-&gt;%(parent.name)s added"
        else:
            fmt = "inheritance line %(tag.name)s-&gt;%(parent.name)s removed"
    elif table == 'tag_config':
        if edit:
            fmt = "tag configuration for %(tag.name)s altered"
        elif create:
            fmt = "new tag: %(tag.name)s"
        else:
            fmt = "tag deleted: %(tag.name)s"
    elif table == 'build_target_config':
        if edit:
            fmt = "build target configuration for %(build_target.name)s updated"
        elif create:
            fmt = "new build target: %(build_target.name)s"
        else:
            fmt = "build target deleted: %(build_target.name)s"
    elif table == 'external_repo_config':
        if edit:
            fmt = "external repo configuration for %(external_repo.name)s altered"
        elif create:
            fmt = "new external repo: %(external_repo.name)s"
        else:
            fmt = "external repo deleted: %(external_repo.name)s"
    elif table == 'tag_external_repos':
        if edit:
            fmt = "external repo entry for %(external_repo.name)s in tag %(tag.name)s updated"
        elif create:
            fmt = "external repo entry for %(external_repo.name)s added to tag %(tag.name)s"
        else:
            fmt = "external repo entry for %(external_repo.name)s removed from tag %(tag.name)s"
    elif table == 'group_config':
        if edit:
            fmt = "group %(group.name)s configuration for tag %(tag.name)s updated"
        elif create:
            fmt = "group %(group.name)s added to tag %(tag.name)s"
        else:
            fmt = "group %(group.name)s removed from tag %(tag.name)s"
    elif table == 'group_req_listing':
        if edit:
            fmt = "group dependency %(group.name)s-&gt;%(req.name)s updated in tag %(tag.name)s"
        elif create:
            fmt = "group dependency %(group.name)s-&gt;%(req.name)s added in tag %(tag.name)s"
        else:
            fmt = "group dependency %(group.name)s-&gt;%(req.name)s dropped from tag %(tag.name)s"
    elif table == 'group_package_listing':
        if edit:
            fmt = "package entry %(package)s in group %(group.name)s, tag %(tag.name)s updated"
        elif create:
            fmt = "package %(package)s added to group %(group.name)s in tag %(tag.name)s"
        else:
            fmt = "package %(package)s removed from group %(group.name)s in tag %(tag.name)s"
    else:
        if edit:
            fmt = "%s entry updated" % table
        elif create:
            fmt = "%s entry created" % table
        else:
            fmt = "%s entry revoked" % table
    time_str = time.asctime(time.localtime(ts))
    parts  = [time_str, fmt % x]
    if who:
        parts.append(who % x)
    if create and x['active']:
        parts.append("[still active]")
    print '   ' + ' '.join(parts)

def main():
    """ The main function."""
    parser = setup_parser()
    args = parser.parse_args()
    if args.username and not args.nofas:
        print 'Last login in FAS:'
        _get_last_website_login(args.username)
    if args.username and not args.nokoji:
        print 'Last action on koji:'
        _get_koji_history(args.username)
    if args.email and not args.nobodhi:
        print 'Last action on Bodhi:'
        print '   Not yet implemented'
    if args.email and not args.nobz:
        print 'Bugzilla information:'
        _get_bugzilla_history(args.email)
    if args.email and not args.nolists:
        print 'Last email on mailing list:'
        _get_last_email_list(args.email)

def setup_parser():
    """
    Set the command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="fedora_active_user")
    # General connection options
    parser.add_argument('--user', dest="username",
                help="FAS username")
    parser.add_argument('--email', dest="email",
                help="FAS or Bugzilla email looked for")
    parser.add_argument('--nofas', action='store_true',
                help="Do not check FAS")
    parser.add_argument('--nokoji', action='store_true',
                help="Do not check koji")
    parser.add_argument('--nolists', action='store_true',
                help="Do not check mailing lists")
    parser.add_argument('--nobodhi', action='store_true',
                help="Do not check bodhi")
    parser.add_argument('--nobz', action='store_true',
                help="Do not check bugzilla")
    parser.add_argument('--verbose', action='store_true',
                help="Gives more info about what's going on")
    parser.add_argument('--debug', action='store_true',
                help="Outputs bunches of debugging info")
    return parser

if __name__ == '__main__':
    try:
        main()
    except Exception, err:
        print err
</code></pre></td></tr></table>
</div> <!-- class=content -->
<div class='footer'>generated  by cgit v0.9.0.2 at 2011-12-06 13:17:51 (GMT)</div>
</div> <!-- id=cgit -->
</body>
</html>
