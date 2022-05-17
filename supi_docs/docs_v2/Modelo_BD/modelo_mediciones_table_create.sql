CREATE TABLE public.estudios_realizados (
    id_estudiorealizado uuid NOT NULL,
    id_salas_planificadas uuid NOT NULL,
    id_quiz_1 uuid NOT NULL,
    respuesta_quiz_1 text NOT NULL,
    id_quiz_2 uuid NOT NULL,
    respuesta_quiz_2 text NOT NULL,
    id_quiz_3 uuid NOT NULL,
    respuesta_quiz_3 text NOT NULL,
    foto_inicial_estudio bytea NOT NULL,
    PRIMARY KEY (id_estudiorealizado)
);

CREATE INDEX ON public.estudios_realizados
    (id_salas_planificadas);
CREATE INDEX ON public.estudios_realizados
    (id_quiz_1);
CREATE INDEX ON public.estudios_realizados
    (id_quiz_2);
CREATE INDEX ON public.estudios_realizados
    (id_quiz_3);


COMMENT ON TABLE public.estudios_realizados
    IS 'Para hacer la auditoría el auditor deberá:
1- Hacer la respuesta de su QUIZ
2- El sistema le mostrará el estudio que debe responder con la modalidad de ingreso que se debe y en ella se dará un valor a como lo detecte el auditor. Puede ser una palabra como QUIEBRE o un número como EL PRECIO o una foto para ver el estante vacío. 
A esto se podrá añadir la foto del detalle que se quiere auditar.

Siempre deberá tomarse la GEO del auditor para tener de base el dato de si el auditor está o no in-situ donde dice estar';

CREATE TABLE public. (
    photo Obj NOT NULL
);


CREATE TABLE public. (
    id_estudiorealizado uuid NOT NULL,
    id_productos_planificados uuid NOT NULL,
    consecutivo Integer NOT NULL,
    resultado String NOT NULL,
    comentario String NOT NULL
);

CREATE INDEX ON public.
    (id_estudiorealizado);
CREATE INDEX ON public.
    (id_productos_planificados);

