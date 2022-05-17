CREATE TABLE public. (
    id_planificacion uuid NOT NULL,
    id_planograma uuid NOT NULL,
    id_estudio uuid NOT NULL,
    id_sala uuid NOT NULL,
    id_product uuid NOT NULL,
    cadena varchar(100) NOT NULL,
    canal varchar(100) NOT NULL,
    direccion varchar(255) NOT NULL,
    comuna varchar(50) NOT NULL,
    geo point NOT NULL,
    consecutivo Integer NOT NULL,
    fecha_i Date NOT NULL,
    fecha_f Date NOT NULL,
    id_variable uuid NOT NULL,
    estado varchar(15) NOT NULL,
    resultado number NOT NULL,
    tiene_cartel Boolean NOT NULL,
    estado String NOT NULL,
    id_user uuid NOT NULL,
    PRIMARY KEY (id_planificacion)
);

CREATE INDEX ON public.
    (id_planograma);
CREATE INDEX ON public.
    (id_estudio);
CREATE INDEX ON public.
    (id_sala);
CREATE INDEX ON public.
    (id_product);
CREATE INDEX ON public.
    (id_variable);


COMMENT ON COLUMN public..id_user
    IS 'Quien hace la planificación
';

CREATE TABLE public.salas_planificadas (
    id_salas_planificadas uuid NOT NULL,
    id_planificacion uuid NOT NULL,
    id_salas uuid NOT NULL,
    auditor uuid_Id_user NOT NULL,
    coordinador uuid_Id_user NOT NULL,
    estado String NOT NULL,
    PRIMARY KEY (id_salas_planificadas)
);

CREATE INDEX ON public.salas_planificadas
    (id_planificacion);
CREATE INDEX ON public.salas_planificadas
    (id_salas);


CREATE TABLE public.poductos_planificados (
    id_productos_planificados uuid NOT NULL,
    id_salas_planificadas uuid NOT NULL,
    id_producto uuid NOT NULL,
    id_variable uuid NOT NULL,
    valor_x_defecto_target String NOT NULL,
    PRIMARY KEY (id_productos_planificados)
);

CREATE INDEX ON public.poductos_planificados
    (id_salas_planificadas);
CREATE INDEX ON public.poductos_planificados
    (id_producto);
CREATE INDEX ON public.poductos_planificados
    (id_variable);

