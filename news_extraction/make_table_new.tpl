%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<title>新闻人物言论_By_SXQL</title>
<p>新闻内容中的人物言论：</p>
<table border="1">
%for row in rows:
  <tr>
	<td width = 10 align="center">{{row[0]}}</td>
	<td width = 100 align="center">{{row[1]}}</td>
	<td width = 1000 align="center">{{row[2]}}</td>
</tr>
%end
</table>

