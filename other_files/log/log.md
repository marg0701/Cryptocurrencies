# Bitácora. Predictor de valores de bolsa

Miembros del equipo:

- Daniel
- Gerardo
- Luis
- Miguel
- Uzmar

## Octubre 23, 2019

El día de hoy, se buscó el "estado del arte" respecto la aplicación que se nos pidió realizar. Posteriormente, se plantearon las siguientes preguntas respecto a dicha aplicación para tener un punto de partida.

- ¿Cuál es tu experiencia invirtiendo?
- ¿Conoces alguna aplicación?, ¿Cuál?, ¿Qué te gustó?
- ¿Qué consideras que es mejor, invertir a corto o largo plazo, o ambas?
- ¿Cuál es tú opinión frente a las inversiones de riesgo?
- ¿Qué mercado te interesa para invertir?, ¿Local?, ¿Global?, ¿Cripto?
- ¿Qué tanto conoces del mercado de tu interés?
- ¿Qué es lo que esperarías de una aplicación como esta?
- ¿Cuál/cuáles son las funciones de mayor interés?
- ¿Qué información te gustaría visualizar en una app?

A continuación se describe la conversación con el "cliente". Se señalan las sentencias más importantes.

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

**Los clientes no tienen ninguna experiencia.** Leyendo un periódico, se dieron cuenta que las criptomonedas están tomando más importancia. No les interesa invertir en mercado de valores en general, **les interesa más las criptomonedas**. Sin embargo, si queremos ayudar a escoger mejores rendimientos, es posible. Vale la pena entrar en Blockchain, pero eso podría ser algo a parte. Han escuchado sobre Bitcoin, y saben que existen más.Les gustaría saber cuánto cuesta y cuánto es necesario invertir para trabajar en este proyecto.

**Comparar series de tiempo de las criptomonedas más "famosas".** Les interesa averiguar sobre las criptomonedas de Bancomer y Facebook. Se les sugirió analizar la moneda Etherum, pero el que exista un control "fijo" de las criptomonedas, hace que estas adquieran un mayor valor, lo que no les agrada de Etherum ya que no tiene un límite, al menos eso es lo que opina el cliente y les gustaría saber más sobre ello.

**Tienen un conocimiento básico sobre inversiones. No tienen conocimiento de aplicaciones parecidas,** sólo hablaron sobre la aplicación de Bancomer, que permite el control de sus cuentas, y de la cuál **les gusta saber sobre sus portafolios.** **Les gustaría ver la proyección a futuro (6 meses por ejemplo).**

**Les gustaría encontrar una correlación con algún factor económico que tuviera que ver con la proyección del Bitcoin. Se les haría muy interesante el rastrear noticias de economía y observar las palabras clave que aparecen en momentos de picos de valores.**

No saben cuál es la comparación de rendimiento de Bancomer respecto a otras, lo único que se tiene en la aplicación de Bancomer son los portafolios en los que es posible invertir, sus riesgos y retornos de inversión, y ya el usuario decide donde invertir. No saben que otras tasas de interes tienen otros bancos.

Están dispuestos a invertir, y no les preocupa demasiado el riesgo.**Quisieran un portafolio del universo de criptomonedas, que diga el riesgo, volatilidad, etc.** Podría existir distintos portafolios que describieran distintos riesgos y volatilidades (grande, mediana, o poca) dependiendo de las criptomonedas y una proyección de cuánto sería la ganancia a cierto tiempo.

**Principal interés es inversión. Les gustaría que la aplicación dijera en qué portafolios vale la pena invertir dependiendo de si quieren ganancias a mediano o largo plazo.**

Se tiene libertad en la toma de decisión.

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

* La aplicación debe ser intuitiva

* La aplicación está enfocada en el mercado de las criptomonedas

* La aplicación debe desplegar el comportamiento mostrado por la serie de tiempo de cada una de las criptomonedas más famosas

* La aplicación deberá tener la función de detección de anomalías para apoyar en la toma de decisiones del usuario

* La aplicación deberá de proporcionar consejos o soporte para que el cliente invierta.

* La aplicación deberá desplegar noticias al detectarse anomalías en el comportamiento de la criptomoneda.

* La aplicación deberá desplegar información sobre los portafolios con los que ya cuentan el usuario.

* La aplicación deberá realizar recomendaciones sobre los portafolios en los que invertir.

* La aplicación debe mostrar el rendimiento de la inversión.

* La aplicación debe mostrar los "Trending topics" de las noticias para apoyar en la toma de decisiones.

* La aplicación deberá analizar y mostrar el comportamiento de 6 criptomonedas (3 volátiles y 3 no volátiles).

* *La aplicación deberá de mostrar las monedas con una mayor relevancia*

En este día, también se realizó un esquema de "caja negra"


## Octubre 24, 2019

Se comenzó con la definición de "user stories".

## Octubre 25, 2019

Exposición de la aplicación, herramientas que se utilizarán, lo que hará o se espera que haga la aplicación, y un modelo de la página final. 

# MEJORAS AL PROYECTO

- Tomar valores predichos con Prophet para utilizarlos en el algoritmo de portafolios.
(Es complicado porque se necesitaría analizar las tablas que se deben utilizar).

- Bot que automatizara el trading de las cryptocurrencies.
- Implementar las noticias de las criptomonedas en el modelo de Facebook Prophet (analisis de sentimientos).