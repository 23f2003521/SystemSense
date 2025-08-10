import { createWebHistory, createRouter } from 'vue-router';


import home from './components/home.vue';
import Login from './components/Login.vue';
import Dashboard from './components/Dashboard.vue';


// import AdminCreateLot from './components/AdminCreateLot.vue';
// import AdminUpdateLot from './components/AdminUpdateLot.vue';
// import AdminDeleteLot from './components/AdminDeleteLot.vue';
// import AdminViewSpots from './components/AdminViewSpots.vue';
// import AdminDeleteSpot from './components/AdminDeleteSpot.vue';
// import AdminUserSearch from './components/AdminUserSearch.vue';
// import AdminLotSearch from './components/AdminLotSearch.vue';
// import AdminSummary from './components/AdminSummary.vue';


// import UserLotSearch from './components/UserLotSearch.vue';
// import UserBooking from './components/UserBooking.vue';
// import UserUpdateBooking from './components/UserUpdateBooking.vue';
// import UserReleaseBooking from './components/UserReleaseBooking.vue';
// import UserProfile from './components/UserProfile.vue';
// import UserSummary from './components/UserSummary.vue';
// import EditProfile from './components/EditProfile.vue';



const routes = [
    { path: "/" , component: home},
    {path: "/login",component: Login},
    {path:"/dashboard",component: Dashboard},
// // USER ROUTES
//     {path: "/user/lot_search", component: UserLotSearch},
//     {path: "/user/booking/:lotid", component: UserBooking},
//     {path:"/user/update_booking/:reservationid",component: UserUpdateBooking},
//     {path:"/user/release_booking/:reservationid",component: UserReleaseBooking},
//     {path: "/user/profile/:userid", component: UserProfile},
//     { path:"/usersummary",component: UserSummary},
//     {path: '/user/edit/:userid', component: EditProfile},
    
// // ADMIN ROUTES
//     { path: '/admin/create_lot', component: AdminCreateLot },
//     { path: '/admin/update_lot/:lotid', component: AdminUpdateLot },
//     { path: '/admin/get_lot/:lotid', component: AdminUpdateLot },
//     { path: '/admin/delete_lot/:lotid', component: AdminDeleteLot },
//     { path: '/admin/view_spot/:spotid', component: AdminViewSpots },
//     { path: '/admin/delete_spot/:spotid', component: AdminDeleteSpot },
//     { path: '/admin/user_search', component: AdminUserSearch },
//     { path: '/admin/lot_search', component: AdminLotSearch },
//     { path:"/adminsummary",component: AdminSummary}
]


export const router =createRouter({
    history: createWebHistory(),
    routes
})
