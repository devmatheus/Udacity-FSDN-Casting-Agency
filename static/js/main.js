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

// ------------------ //

$('.select2').select2();

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