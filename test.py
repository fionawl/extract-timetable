
def makeTags(tag):
	return ("<" + tag + ">", "</" + tag + ">")



def extract_val(s):
	i = 0

	while (i < len (s)):
		if s[i] == '>':
			start = i
			end = s[i+1:].index('<') + i
			if end - start > 1:
				return s[start+1:end+1]
		i = i + 1
	return s

print(extract_val("<><><>hello<>"))


def extract(s, tag):
	if s != None:
		tags = makeTags(tag)
		print(tags)
		innerContent = []
		unprocessed = s.split(tags[0])[1]

		print(unprocessed)
		unprocessed = s.split(tags[0][:-1])   # ele in unprocessed:
												# " align="LEFT">content</td>"
		print(unprocessed)
		del unprocessed[0]

		print(unprocessed)
		for thing in unprocessed:               # ele in unprocessed
			thang = s0[s0.index(">") + 1:]      # "content</td>"
			thang.split(tags[1])                # extracts "content"
			innerContent.append(thang)
		return innerContent
	return s 

s = "<td>this is the content</td>"
print(extract(s, "tr"))
