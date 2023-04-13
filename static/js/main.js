import EntityCRUD from './entity_crud.js';
import ActorCRUD from './actor_crud.js';
import MovieCRUD from './movie_crud.js';

const actorCRUD = new ActorCRUD();
const movieCRUD = new MovieCRUD();

function getIdFromUrl(entity) {
    const regex = new RegExp(`/${entity}/(\\d+)/edit`);
    const match = window.location.pathname.match(regex);
    return match ? parseInt(match[1], 10) : null;
}

const editActorId = getIdFromUrl('actors');
if (editActorId) {
    actorCRUD.edit(editActorId);
}

const editMovieId = getIdFromUrl('movies');
if (editMovieId) {
    movieCRUD.edit(editMovieId);
}

const actorForm = document.getElementById('actor-form');
if (actorForm) {
    actorForm.addEventListener('submit', actorCRUD.save);
}

const movieForm = document.getElementById('movie-form');
if (movieForm) {
    movieForm.addEventListener('submit', movieCRUD.save);
}

const deleteActorButtons = document.querySelectorAll('.delete-actor');
if (deleteActorButtons) {
    deleteActorButtons.forEach(button => {
        button.addEventListener('click', actorCRUD.delete);
    });
}

const deleteMovieButtons = document.querySelectorAll('.delete-movie');
if (deleteMovieButtons) {
    deleteMovieButtons.forEach(button => {
        button.addEventListener('click', movieCRUD.delete);
    });
}

const actorTable = document.getElementById('actor-table');
if (actorTable) {
    actorCRUD.list(actorTable);
}

const movieTable = document.getElementById('movie-table');
if (movieTable) {
    movieCRUD.list(movieTable);
}
