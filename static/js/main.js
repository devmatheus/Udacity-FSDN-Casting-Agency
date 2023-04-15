import { getIdFromUrl } from './utils.js';
import { ActorCRUD } from './actor_crud.js';
import { MovieCRUD } from './movie_crud.js';

function instantiateCRUDClasses() {
    const currentPath = window.location.pathname;

    if (currentPath.startsWith('/actors')) {
        return new ActorCRUD();
    } else if (currentPath.startsWith('/movies')) {
        return new MovieCRUD();
    }

    return null;
}

window.crudInstance = instantiateCRUDClasses();

const editId = getIdFromUrl('actors') || getIdFromUrl('movies');
if (editId) {
    crudInstance.fetchEntity(editId)
    .then((entity) => {
        crudInstance.populateForm(entity.data);
    });
        
}

const form = document.getElementById('actor-form') || document.getElementById('movie-form');
if (form) {
    form.addEventListener('submit', crudInstance.save);
}

const deleteButtons = document.querySelectorAll('.delete-actor,.delete-movie');
if (deleteButtons) {
    deleteButtons.forEach(button => {
        button.addEventListener('click', crudInstance.delete);
    });
}

const table = document.getElementById('actor-table') || document.getElementById('movie-table');
if (table) {
    crudInstance.list(table);
}

// ------------------ //

function setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-link');

    navItems.forEach((navItem) => {
        const itemRoute = navItem.getAttribute('href');
        if (currentPath == itemRoute) {
            navItem.classList.add('active');
        } else {
            navItem.classList.remove('active');
        }
    });
}

setActiveNavItem();