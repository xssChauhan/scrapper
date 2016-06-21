def closestMatch(s , obj , session , attr = "name"):
    match = {
        "s" : 0,
        "p" : 0
    }
    toMatch = [ " ".join(s.split()[:e]) for e in xrange(1, len(s.split()) + 1) ]
        

    for e in xrange(len(toMatch)//2 - 1,len(toMatch)):
        i = obj.likeAll(toMatch[e],attr,session)
        for t in i:
            if not isinstance(t,NoneType):
                score = (tsor(s,t.name),pr(s,t.name))
                if score > (match['s'],match['p']):
                    match['s'] , match['p'] = score
                    match['d'] = t
    return match
