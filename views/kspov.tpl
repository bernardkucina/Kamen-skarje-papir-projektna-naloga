%import model
%rebase('views/base.tpl')

<h3>KAMEN ŠKARJE PAPIR OGENJ VODA</h3>

<BLOckquote>
    Dobrodošli v igri Kamen Škarje Papir. Igrali boste proti računalniku.
    Igralo se bo minimalno 7 iger.
    Igra se točkuje: igralec : računalnik
</BLOckquote>

<div class="rezultat1">
    <h2>{{igra.delni_izid_igralca()}} : {{igra.delni_izid_racunalnika()}}</h2>
</div>

<div class="radio">
    <form action="/ksp/" method="POST">
        <input type="radio" name="orozje" value="0" id="kamen">
        <label for="kamen">KAMEN</label>

        <input type="radio" name="orozje" value="1" id="skarje">
        <label for="skarje">ŠKARJE</label>

        <input type="radio" name="orozje" value="2" id="papir">
        <label for="papir">PAPIR</label>

        <input type="radio" name="orozje" value="3" id="ogenj">
        <label for="ogenj">OGENJ</label>
        
        <input type="radio" name="orozje" value="4" id="voda">
        <label for="voda">VODA</label>

        <button type="submit" class="potrdi">Potrdi</button>
    </form>
</div>

% if igra.zmaga_igralca_1() == True:
<div class="center">
    <div class="content">
        <div class="glava zmaga">
            <h2>ZMAGA</h2>
        </div>
        <P>BRAVO, ZMAGAL SI MOGOČNI STROJ Z IZIDOM {{igra.koncni_izid_igralca_1()}} : {{igra.koncni_izid_racunalnika_1()}}</P>
        <form action="/" method="GET">
            <button type="submit" class="zacetni">ZACETNI MENI</button>
        </form>
    </div>
</div>
%end

% if igra.zmaga_racunalnika_1() == True:
<div class="center">
    <div class="content">
        <div class="glava poraz">
            <h2>PORAZ</h2>
        </div>
        <P>IZGUBIL SI PROTI RAČUBALNIKU Z IZIDOM {{igra.koncni_izid_igralca_1()}} : {{igra.koncni_izid_racunalnika_1()}}</P>
        <form action="/" method="GET">
            <button type="submit" class="zacetni">ZACETNI MENI</button>
        </form>
    </div>
</div>
%end





