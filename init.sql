BEGIN;
SET client_encoding = 'UTF8';

CREATE TABLE db_pokemons (
    id_pokemon integer NOT NULL,
    name text NOT NULL,
    base_experience integer NOT NULL,
    weight integer NOT NULL,
    height integer NOT NULL,
    is_default boolean not null,
    PRIMARY KEY (id_pokemon)
);
CREATE TABLE db_abilities (
    id_ability integer NOT NULL,
    name text NOT NULL,
    effect_entries text NOT NULL,
    PRIMARY KEY (id_ability)
);
CREATE TABLE db_types (
    id_type integer NOT NULL,
    name text NOT NULL,
    damage_relations json,
    PRIMARY KEY (id_type)
);
CREATE TABLE db_vinc_pokemon_ability(
    id_pokemon integer not null,
    id_ability integer not null
);

CREATE TABLE db_vinc_pokemon_type(
    id_pokemon integer not null,
    id_type integer not null
);

ALTER TABLE ONLY db_vinc_pokemon_ability
    ADD CONSTRAINT vinc_pokemon_fkey FOREIGN KEY (id_pokemon) REFERENCES db_pokemons(id_pokemon) ON DELETE CASCADE,
    ADD CONSTRAINT vinc_ability_fkey FOREIGN KEY (id_ability) REFERENCES db_abilities(id_ability) ON DELETE CASCADE;

ALTER TABLE ONLY db_vinc_pokemon_type
    ADD CONSTRAINT vinc_pokemon_fkey FOREIGN KEY (id_pokemon) REFERENCES db_pokemons(id_pokemon) ON DELETE CASCADE,
    ADD CONSTRAINT vinc_type_fkey FOREIGN KEY (id_type) REFERENCES db_types(id_type) ON DELETE CASCADE;

COMMIT;

ANALYZE db_pokemons;
ANALYZE db_abilities;
ANALYZE db_types;
ANALYSE db_vinc_pokemon_ability;
ANALYSE db_vinc_pokemon_type;

