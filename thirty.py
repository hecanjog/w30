from pippi import dsp
from pippi import tune
import audioop

thirty = dsp.read('thirty.wav').data
wesley = dsp.read('wesley.wav').data
snds = [thirty, wesley]

## 01
out = ''
t = thirty * 30
t = dsp.pan(t, 0)

tt = dsp.cut(thirty, 0, dsp.flen(thirty) - dsp.mstf(30)) * 30
tt = dsp.pan(tt, 1)

out = dsp.mix([ t, tt ])
dsp.write(out, 'wesley_thirty_01')

## 02
out = ''
t = dsp.split(thirty, dsp.mstf(40))
t = [ dsp.env(tt, 'sine') for tt in t ]
t = [ tt * 4 for tt in t ]

out = ''.join(t)

dsp.write(out, 'wesley_thirty_02')

## 03
out = ''

freqs = tune.fromdegrees([1, 3, 5, 9], 3, 'c')
layers = []
for i in range(30):
    l = dsp.pine(dsp.amp(thirty, 0.1), dsp.stf(30), dsp.randchoose(freqs))
    l = dsp.pan(l, dsp.rand())
    layers += [ l ]

out = dsp.mix(layers)

dsp.write(out, 'wesley_thirty_03')

## 04
out = ''

for count in range(30):
    t = dsp.randchoose(snds)
    t = dsp.vsplit(t, 1, dsp.mstf(20))
    for i, g in enumerate(t):
        if dsp.randint(0,5) == 0:
            t[i] = g * dsp.randint(1, 30)

        t[i] = dsp.pan(t[i], dsp.rand())

    out += ''.join(t)

dsp.write(out, 'wesley_thirty_04')

## 05
out = ''
freqs = tune.fromdegrees([1, 3, 5, 9], 3, 'c')
freqs2 = tune.fromdegrees([8, 6, 3, 1], 3, 'c')
slen = dsp.flen(wesley) / 30
ww = dsp.split(wesley, slen)

for i in range(30):
    freq = freqs[i % len(freqs)]
    w = dsp.pine(ww[i], dsp.mstf(300), freq)

    freq2 = freqs2[i % len(freqs2)]
    w2 = dsp.pine(ww[i], dsp.mstf(300), freq2)
    out += dsp.mix([ w, w2 ])

dsp.write(out, 'wesley_thirty_05')

## 06
out = ''
freqs = tune.fromdegrees([1, 3, 5, 12], 3, 'c')
freqs2 = tune.fromdegrees([9, 6, 5, 1], 3, 'c')
slen = dsp.flen(thirty) / 30
tt = dsp.split(thirty, slen)

for i in range(30):
    freq = freqs[i % len(freqs)]
    t = dsp.pine(tt[i], dsp.mstf(300), freq)

    freq2 = freqs2[i % len(freqs2)]
    t2 = dsp.pine(tt[i], dsp.mstf(300), freq2)
    out += dsp.mix([ t, t2 ])

dsp.write(out, 'wesley_thirty_06')

## 07
out = ''

w = dsp.vsplit(wesley, 1, 30)
for i, g in enumerate(w):
    w[i] = g * dsp.randint(1, 30)
    w[i] = dsp.pan(w[i], dsp.rand())

out = ''.join(w)

dsp.write(out, 'wesley_thirty_07')

## 08
out = ''

w = dsp.vsplit(wesley, dsp.mstf(40), dsp.mstf(80))
for i, g in enumerate(w):
    gg = ''
    for n in range(dsp.randint(1, 30)):
        gg += dsp.amp(dsp.env(dsp.pan(g, dsp.rand()), 'sine'), dsp.rand())

    w[i] = gg

out = ''.join(w)

dsp.write(out, 'wesley_thirty_08')

## 09
out = ''
t = dsp.split(thirty, 5)
freqs = tune.fromdegrees([1, 3, 5, 9], 2, 'c')
layers = []

for freq in freqs:
    l = [ dsp.env(tt, 'phasor') for tt in t ]
    l = [ dsp.pad(tt, 0, dsp.htf(freq) - 5) for tt in l ]
    l = ''.join(l)
    l = dsp.pan(l, dsp.rand())
    layers += [ l ]

out = dsp.mix(layers)

dsp.write(out, 'wesley_thirty_09')

## 10
out = ''
lens = tune.fromdegrees([1,2,3,4,5,6,8,9], 1, 'c')
lens = [ dsp.htf(ll) - 1 for ll in lens ]

w = dsp.split(wesley, 1)
w = [ ww for i, ww in enumerate(w) if i % 30 == 0 ]
w = [ dsp.pad(ww, 0, dsp.randchoose(lens) / dsp.randint(1, 3)) for ww in w ]
w = [ ww * dsp.randint(0, 10) for ww in w ]
w = [ dsp.pan(ww, dsp.rand()) for ww in w ]
w = [ dsp.amp(ww, dsp.rand(1, 30)) for ww in w ]
out = ''.join(w)

dsp.write(out, 'wesley_thirty_10')

## 11
out = ''
curves = [ dsp.breakpoint([ dsp.rand() for p in range(3) ], 30) for c in range(30) ]

for curve in curves:
    clen = dsp.mstf(30)
    s = dsp.randchoose(snds)
    t = [ dsp.cut(s, dsp.flen(s) * c - clen, clen) for c in curve ]
    t = [ dsp.env(tt, 'sine') for tt in t ]
    t = [ dsp.pan(t[i], curve[i]) for i, c in enumerate(curve) ]
    curve.reverse()
    t = [ dsp.transpose(t[i], (curve[i] * 0.5) + 0.75) for i, c in enumerate(curve) ]
    t = ''.join(t)
    out += t

dsp.write(out, 'wesley_thirty_11')

## 12
out = ''

wlen = dsp.flen(wesley) / 100
w = dsp.split(wesley, wlen)

min_speeds = dsp.curve(4, 30)
min_speeds = [ (m * 0.75) + 0.25 for m in min_speeds ]

for rep in range(30):
    curves = [ dsp.breakpoint([ dsp.rand(min_speeds[rep], 1.5) for p in range(10) ], 100) for c in range(30) ]
    layers = []
    for curve in curves:
        ww = [ dsp.transpose(w[i], curve[i]) for i in range(100) ]
        ww = ''.join(ww)
        ww = dsp.pan(ww, dsp.rand())
        layers += [ ww ]

    out += dsp.mix(layers)

dsp.write(out, 'wesley_thirty_12')

## 13
out = ''

layers = []

for l in range(30):
    w = dsp.vsplit(wesley, 30, 300)

    for i, ww in enumerate(w):
        choice = dsp.randint(0, 3)

        if choice == 0:
            www = ''
            reps = dsp.randint(10, 100)
            pans = dsp.breakpoint([ dsp.rand() for p in range(reps / 3) ], reps)
            for m in range(reps):
                www += dsp.pan(ww, pans[m])

            w[i] = www

        elif choice == 1:
            w[i] = dsp.transpose(ww, dsp.rand(0.1, 0.75))
            w[i] = dsp.pan(w[i], dsp.rand())

        elif choice == 2:
            w[i] = dsp.fill(ww, dsp.mstf(200))
            w[i] = dsp.pine(w[i], dsp.mstf(dsp.randint(300, 1000)), dsp.rand(50, 2000))

        elif choice == 3:
            pass

    layers += [ dsp.amp(''.join(w), 0.5) ]

out = dsp.mix(layers)

dsp.write(out, 'wesley_thirty_13')

## 14
out = ''

for i in range(30):
    t = dsp.split(thirty, dsp.mstf(30))
    for i, tt in enumerate(t):
        if dsp.randint(0, 1) == 0 and i > 0:
            t.insert(i - 1, tt)

    if dsp.randint(0, 1) == 0:
        t.reverse()

    t = [ dsp.alias(tt) for tt in t ]

    out += ''.join(t)

dsp.write(out, 'wesley_thirty_14')

## 15
out = ''

freqs = tune.fromdegrees([1, 3, 5, 9], 3, 'c')

lens = [ 1, 1.25, 1.5, 2, 3, 5, 10, 20 ]
for plen in lens:
    layers = []
    for freq in freqs:
        l = dsp.pine(dsp.amp(thirty, 0.5), int(dsp.flen(thirty) * plen), freq)
        l = dsp.pan(l, dsp.rand())
        layers += [ l ]

    out += dsp.mix(layers)

dsp.write(out, 'wesley_thirty_15')

## 16
out = ''

def make_pulses(degrees, bpm):
    freqs = tune.fromdegrees(degrees, 3, 'c')

    layers = []
    for freq in freqs:
        l = dsp.pine(dsp.amp(thirty, 0.5), int(dsp.flen(thirty) * 20), freq)
        l = dsp.pan(l, dsp.rand())
        layers += [ l ]

    t = dsp.mix(layers)

    t = dsp.split(t, dsp.mstf(dsp.bpm2ms(bpm)))

    t = dsp.randshuffle(t)

    return ''.join(t)

out += make_pulses([1, 3, 5, 9], 200)
out += make_pulses([1, 3, 6, 8], 200)
out += make_pulses([1, 3, 5, 6 + 12], 400)
out += dsp.cut(make_pulses([1, 3, 5, 6 + 12], 1200), 0, dsp.stf(2.5))

dsp.write(out, 'wesley_thirty_16')

## 17
out = ''

freqs = tune.fromdegrees([1, 3, 5, 9], 8, 'c')

layers = []
for freq in freqs:
    l = dsp.pine(dsp.amp(thirty, 0.5), dsp.stf(5), freq)
    l = dsp.pan(l, dsp.rand())
    layers += [ l ]

out = dsp.mix(layers)

dsp.write(out, 'wesley_thirty_17')

## 18
out = ''
upper = [ dsp.randint(60, 200) for i in range(10) ]
upper += [ dsp.randint(20, 60) for i in range(30) ]
upper += [ dsp.randint(5, 20) for i in range(10) ]
upper += [3, 1, 0]

for up in upper:
    w = dsp.vsplit(wesley, 30, 300)
    for i, ww in enumerate(w):
        if dsp.randint(0, up) != 0:
            w[i] = dsp.pad('', 0, dsp.flen(ww))

    out += ''.join(w)

dsp.write(out, 'wesley_thirty_18')

## 19
out = ''
upper = [2, 4]
upper += [ dsp.randint(5, 20) for i in range(10) ]
upper += [ dsp.randint(20, 60) for i in range(30) ]
upper += [ dsp.randint(60, 200) for i in range(10) ]

for up in upper:
    w = dsp.vsplit(thirty, 30, 300)
    for i, ww in enumerate(w):
        if dsp.randint(0, up) != 0:
            w[i] = dsp.pad('', 0, dsp.flen(ww))

    out += ''.join(w)

dsp.write(out, 'wesley_thirty_19')

## 20
out = ''

w = dsp.split(wesley, 30)
speeds = dsp.curve(4, len(w))
for i, ww in enumerate(w):
    w[i] = dsp.transpose(ww, speeds[i] + 0.01)

out = ''.join(w)

dsp.write(out, 'wesley_thirty_20')

## 21
out = ''

for r in range(2):
    w = dsp.split(wesley, 30)
    speeds = dsp.breakpoint([ dsp.rand(0.01, 1.1) for i in range(len(w) / 10) ], len(w))
    for i, ww in enumerate(w):
        w[i] = dsp.transpose(ww, speeds[i])

    out += ''.join(w)

dsp.write(out, 'wesley_thirty_21')

## 30 
out = ''
w = wesley * 30
w = dsp.pan(w, 0)

ww = dsp.cut(wesley, 0, dsp.flen(wesley) - dsp.mstf(30)) * 30
ww = dsp.pan(ww, 1)

out = dsp.mix([ w, ww ])

dsp.write(out, 'wesley_thirty_30')
