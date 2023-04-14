export function getIdFromUrl(entity) {
    const regex = new RegExp(`/${entity}/(\\d+)/edit`);
    const match = window.location.pathname.match(regex);
    return match ? parseInt(match[1], 10) : null;
}
