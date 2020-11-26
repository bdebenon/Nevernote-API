create table notes
(
    id            serial not null
        constraint notes_pk
            primary key,
    title         varchar(255),
    body          text,
    created       timestamp,
    last_modified timestamp
);

alter table notes
    owner to postgres;

create table notebooks
(
    id    serial not null
        constraint notebooks_pk
            primary key,
    title varchar(255)
);

alter table notebooks
    owner to postgres;

create table junction_notebooks_notes
(
    notebook_id integer not null
        constraint join_notebooks_notes_notebooks_id_fk
            references notebooks
            on update cascade on delete cascade,
    note_id     integer not null
        constraint join_notebooks_notes_notes_id_fk
            references notes
            on update cascade on delete cascade,
    constraint join_notebooks_notes_pk
        primary key (notebook_id, note_id)
);

alter table junction_notebooks_notes
    owner to postgres;

create table tags
(
    tag varchar(255) not null
        constraint tags_pk
            primary key
);

alter table tags
    owner to postgres;

create table junction_notes_tags
(
    note_id integer      not null
        constraint junction_notes_tags_notes_id_fk
            references notes
            on update cascade on delete cascade,
    tag     varchar(255) not null
        constraint junction_notes_tags_tags_tag_fk
            references tags
            on update cascade on delete cascade,
    constraint junction_notes_tags_pk
        primary key (note_id, tag)
);

alter table junction_notes_tags
    owner to postgres;

