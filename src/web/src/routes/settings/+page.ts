import type {PageLoad} from "./$types";
import {redirect} from "@sveltejs/kit";

export const load = (async () => {
    throw redirect(307, "/settings/alarm");
}) satisfies PageLoad;
