CREATE TABLE public.users (
    id_user uuid NOT NULL,
    tipo integer NOT NULL,
    nombreuser varchar(255) NOT NULL,
    currentgps point NOT NULL,
    PRIMARY KEY (id_user)
);


COMMENT ON TABLE public.users
    IS 'Se manejarán 4 perfiles:

1- Clientes
2- Auditores. (los que están en la calle)
3- Auditores de campo (los que están en los departamentos. Son los jefes)
4- Coordinadores
';

CREATE TABLE public.salas (
    id_planograma uuid NOT NULL,
    id_sala uuid NOT NULL,
    nombresala varchar(100) NOT NULL,
    comuna varchar(100) NOT NULL,
    geo point NOT NULL,
    logo_cadena Image NOT NULL,
    nombre_cadena String NOT NULL,
    PRIMARY KEY (id_sala)
);

CREATE INDEX ON public.salas
    (id_planograma);


CREATE TABLE public.variables (
    id_variable uuid NOT NULL,
    nombrevariable varchar(100) NOT NULL,
    label_visual String NOT NULL,
    tipo_dato integer NOT NULL,
    objeto_componente_visual bytea NOT NULL,
    valores_combobox String NOT NULL,
    PRIMARY KEY (id_variable)
);


COMMENT ON TABLE public.variables
    IS 'tabla creada para manejar las variables que se miden: 

1 OSA (Presencia)
2 Precios
3 Facing, Sovi
4 Cartelería
5 Exhibiciones';
COMMENT ON COLUMN public.variables.tipo_dato
    IS '1 OSA (Presencia)
2 Precios
3 Facing, Sovi
4 Cartelería
5 Exhibiciones';

CREATE TABLE public.photo (
    id_photo uuid NOT NULL,
    nombrephoto varchar(100) NOT NULL,
    archivo bytea NOT NULL,
    PRIMARY KEY (id_photo)
);


COMMENT ON TABLE public.photo
    IS 'archivo que se toma y registra en el sistema y se podrá consultar varias veces antes de ser enviado. Editado y nombrado.';

CREATE TABLE public.estudios (
    id_estudio uuid NOT NULL,
    id_variable  NOT NULL,
    nombreestudio varchar(100) NOT NULL,
    PRIMARY KEY (id_estudio)
);

CREATE INDEX ON public.estudios
    (id_variable);


CREATE TABLE public.clientes (
    id_client uuid NOT NULL,
    nombre varchar(255) NOT NULL,
    rut String NOT NULL,
    region varchar(100) NOT NULL,
    PRIMARY KEY (id_client)
);


CREATE TABLE public.productos (
    id_product uuid NOT NULL,
    ean String NOT NULL,
    nombre String NOT NULL,
    foto Obj NOT NULL,
    PRIMARY KEY (id_product)
);


CREATE TABLE public.quiz (
    id_quiz uuid NOT NULL,
    id_estudio uuid NOT NULL,
    id_client  NOT NULL,
    consecutivo Integer NOT NULL,
    nombrequiz varchar(255) NOT NULL,
    pregunta text NOT NULL,
    opcion_respuesta1_correcta text NOT NULL,
    opcion_respuesta2 text NOT NULL,
    opcion_respuesta3 text NOT NULL,
    PRIMARY KEY (id_quiz)
);

CREATE INDEX ON public.quiz
    (id_estudio);
CREATE INDEX ON public.quiz
    (id_client);


COMMENT ON TABLE public.quiz
    IS 'Constituído para dar soporte a las preguntas y posibles respuestas que se le har+an a los auditores para saber si pueden enfrentar o no su auditoría.';
COMMENT ON COLUMN public.quiz.opcion_respuesta1_correcta
    IS 'Esta siempre es la respuesta correcta';

CREATE TABLE public.muebles (
    id_mueble uuid NOT NULL,
    nombre varchar NOT NULL,
    puerta numeric NOT NULL,
    marca varchar NOT NULL,
    division numeric NOT NULL,
    bandeja numeric NOT NULL,
    PRIMARY KEY (id_mueble)
);

