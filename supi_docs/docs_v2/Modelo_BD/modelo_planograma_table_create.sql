CREATE TABLE public.planograma (
    id_planograma uuid NOT NULL,
    id_client uuid NOT NULL,
    id_estudio uuid NOT NULL,
    consecutivo Integer NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date NOT NULL,
    valor_historico numeric NOT NULL,
    base varchar(100) NOT NULL,
    target varchar(100) NOT NULL,
    id_area uuid NOT NULL,
    id_user uuid NOT NULL,
    PRIMARY KEY (id_planograma)
);

CREATE INDEX ON public.planograma
    (id_client);
CREATE INDEX ON public.planograma
    (id_estudio);
CREATE INDEX ON public.planograma
    (id_area);


COMMENT ON COLUMN public.planograma.id_user
    IS 'Quien hace el planograma';

CREATE TABLE public.salas_del_planograma (
    id_sala_planogramada uuid NOT NULL,
    id_planograma uuid NOT NULL,
    id_sala uuid NOT NULL,
    PRIMARY KEY (id_sala_planogramada)
);

CREATE INDEX ON public.salas_del_planograma
    (id_planograma);
CREATE INDEX ON public.salas_del_planograma
    (id_sala);


CREATE TABLE public. (
    producto_planogramado uuid NOT NULL,
    id_sala_planogramada uuid NOT NULL,
    id_product uuid NOT NULL,
    id_variable uuid NOT NULL,
    valor_x_defecto_target String NOT NULL,
    PRIMARY KEY (producto_planogramado)
);

CREATE INDEX ON public.
    (id_sala_planogramada);
CREATE INDEX ON public.
    (id_product);
CREATE INDEX ON public.
    (id_variable);

