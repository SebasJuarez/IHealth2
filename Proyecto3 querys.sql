-- creacion de index
CREATE INDEX idx_userid 
ON usuario(user_id);

CREATE INDEX idx_inst_id
ON instructor(inst_id);

CREATE INDEX idx_cursoid
ON cursos(curso_id);

CREATE INDEX idx_s_userid 
ON sesiones(user_id);

CREATE INDEX idx_s_instid 
ON sesiones(inst_id);

CREATE INDEX idx_s_cursoid 
ON sesiones(curso_id);
-- creacion de la bitacora
create table auditoria(
	acc_type varchar (20),
	nombre varchar (15),
	user_id integer,
	fecha_cre date,
	CONSTRAINT user_id
       FOREIGN KEY(user_id) 
       REFERENCES usuario(user_id)
)

-- modificaciones bitacora
ALTER TABLE auditoria
DROP CONSTRAINT user_id;
select * from usuario

select distinct user_id from auditoria order by user_id

ALTER TABLE auditoria 
ADD COLUMN tabla VARCHAR;

ALTER TABLE auditoria 
ADD COLUMN curso_id integer;

ALTER TABLE auditoria 
ADD COLUMN inst_id integer;

ALTER TABLE auditoria 
    ALTER COLUMN tabla TYPE VARCHAR (100)
ALTER TABLE auditoria 
    ALTER COLUMN nombre TYPE VARCHAR (100)

-- modificaciones sesiones
ALTER TABLE sesiones 
ADD COLUMN calorias integer;
ALTER TABLE sesiones 
ADD COLUMN cur_nom varchar(50);

-- Parte de los triggers del usuario.
create FUNCTION VALIDACION_ASIGNACION()
RETURNS TRIGGER AS $$
DECLARE
	total_asignaciones INT; -- Esta variable almacenara el total de asignaciones actuales
BEGIN
	insert into auditoria (acc_type, nombre, user_id, fecha_cre, tabla) 
	values(new.acc_type,new.nombre,new.user_id,current_timestamp, 'usuario');
	
	RETURN NEW;--Hasta este momento se realizara el insert
END;
$$ LANGUAGE PLPGSQL;

DROP FUNCTION VALIDACION_ASIGNACION cascade

create trigger insertar_bitacora 
before Update
on usuario 
for each row
	execute procedure VALIDACION_ASIGNACION();

create trigger insertar_bitacora2 
before insert
on usuario 
for each row
	execute procedure VALIDACION_ASIGNACION();

create trigger insertar_bitacora3 
before Delete
on usuario 
for each row
	execute procedure VALIDACION_ASIGNACION();
	
-- Parte de los triggers para instructor

CREATE FUNCTION VALIDACION_ASIGNACION2()
RETURNS TRIGGER AS $$
DECLARE
	total_asignaciones INT;
BEGIN
	insert into auditoria (acc_type, nombre, fecha_cre, tabla, inst_id) 
	values('Admin_1,4',new.inst_nombre,current_timestamp, 'instructor', new.inst_id);
	
	RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;

drop function VALIDACION_ASIGNACION2 cascade

create trigger insertar_bitacora 
before Update
on instructor 
for each row
	execute procedure VALIDACION_ASIGNACION2();

create trigger insertar_bitacora2 
before insert
on instructor 
for each row
	execute procedure VALIDACION_ASIGNACION2();

create trigger insertar_bitacora3 
before Delete
on instructor
for each row
	execute procedure VALIDACION_ASIGNACION2();
	
-- Parte de los triggers para sesiones

CREATE FUNCTION VALIDACION_ASIGNACION3()
RETURNS TRIGGER AS $$
DECLARE
	total_asignaciones INT;
BEGIN
	insert into auditoria (acc_type, nombre, user_id, fecha_cre, tabla) 
	values('Miembro',new.categoria,new.user_id,current_timestamp, 'sesiones');
	
	RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;

drop function VALIDACION_ASIGNACION3 cascade

create trigger insertar_bitacora 
before Update
on sesiones 
for each row
	execute procedure VALIDACION_ASIGNACION3();

create trigger insertar_bitacora2 
before insert
on sesiones 
for each row
	execute procedure VALIDACION_ASIGNACION3();

create trigger insertar_bitacora3 
before Delete
on sesiones
for each row
	execute procedure VALIDACION_ASIGNACION3();

-- Parte de los triggers para los cursos

CREATE FUNCTION VALIDACION_ASIGNACION4()
RETURNS TRIGGER AS $$
DECLARE
	total_asignaciones INT;
BEGIN
	insert into auditoria (acc_type, nombre, fecha_cre, tabla, curso_id) 
	values('Admin_2,4',new.descripcion,current_timestamp, 'cursos', new.curso_id);
	
	RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;

drop function VALIDACION_ASIGNACION4 cascade

create trigger insertar_bitacora 
before Update
on cursos
for each row
	execute procedure VALIDACION_ASIGNACION4();

create trigger insertar_bitacora2 
before insert
on cursos 
for each row
	execute procedure VALIDACION_ASIGNACION4();

create trigger insertar_bitacora3 
before Delete
on cursos
for each row
	execute procedure VALIDACION_ASIGNACION4();
	
select * from auditoria
select * from usuario
select * from sesiones
select * from cursos
select * from instructor