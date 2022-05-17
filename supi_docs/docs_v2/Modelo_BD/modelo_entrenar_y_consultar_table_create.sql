CREATE TABLE public.photo_training_upload (
    id_photo uuid NOT NULL,
    id_user uuid NOT NULL,
    result varchar(300) NOT NULL,
    date_sent date NOT NULL
);

CREATE INDEX ON public.photo_training_upload
    (id_photo);
CREATE INDEX ON public.photo_training_upload
    (id_user);


COMMENT ON TABLE public.photo_training_upload
    IS 'El campo result será lo que devuelva la vision artificial.
Date sent es la fecha exatta y time enviado.

Los parámetros y sus ejemplos están faltantes para presentar
';
