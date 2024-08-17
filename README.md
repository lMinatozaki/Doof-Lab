### Doofenshmirtz Evil INC.: Proyecto de Base de datos No Relacionales

<a href="#"><img width="20%" height="auto" src="https://upload.wikimedia.org/wikipedia/en/d/dc/Perry_the_Platypus.png" height="175px"/></a>

Laboratorio Doofenshmirtz desea una aplicación web que les permita
gestionar su catálogo de exámenes y servicios. En este sentido, desean
que la aplicación permita:
1) Gestionar exámenes y servicios: En esta opción, se podrá crear,
modificar y eliminar un examen o servicio. De cada uno de ellos se saben
sus datos básicos: un código identificador único, una categoría a la que
pertenecen, el tipo de muestra del mismo, el precio (en Bs) y las
indicaciones pertenecientes al examen o servicio. Las indicaciones
también podrán crearse, modificarse y eliminarse, y la aplicación deberá
estar en capacidad de permitir al usuario seleccionar una de las
indicaciones ya creadas al crear un examen, o bien, crear una nueva si
llegase a ser necesario.
2) Gestionar categorías: Esta opción permitirá al usuario crear, modificar
y eliminar categorías de exámenes. Por cada categoría se contará con
su nombre y descripción, y esta categoría es la que seleccionará el
usuario cuando esté registrando el examen o servicio.
3) Consultar catálogo: Esta opción permitirá al usuario listar todos los
exámenes y servicios, pudiendo filtrarlos por su categoría o por tipo de
muestra. Este listado deberá ofrecerse en una tabla, que por cada
examen indicará su código, nombre y precio, además de las opciones:
Consultar, modificar y eliminar. Además de esto, cada examen deberá
poder ser consultado de manera individual.
4) Ver reporte: Esta opción generará un reporte, en el cual se podrán
visualizar:
- Cuántos exámenes hay registrados en cada categoría.
- Cuál es la indicación de examen más común.
- Una lista que agrupe los exámenes por precio según el intervalo de: 1 -
100 bs, 101 - 200 bs, 201 - 300 bs, 301 - 500 bs, 501+ bs. Esta lista deberá
indicar cuántos exámenes hay en cada intervalo.
