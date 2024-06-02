import Vue from 'vue';
import Router from 'vue-router';

import AdminManagement from './vue_components/admin_management.vue';
import Bookmark from './vue_components/bookmark.vue';
import BusinessClaim from './vue_components/business_claim.vue';
import BusinessDetail from './vue_components/business_detail.vue';
import BusinessListing from './vue_components/business_listing.vue';
import Review from './vue_components/review.vue';
import SpecialOffer from './vue_components/special_offer.vue';
import TrendingTag from './vue_components/trending_tag.vue';
import UserLogin from './vue_components/user_login.vue';
import UserRegistration from './vue_components/user_registration.vue';
import NotFoundComponent from './vue_components/not_found.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/admin-management',
      name: 'AdminManagement',
      component: AdminManagement
    },
    {
      path: '/bookmark',
      name: 'Bookmark',
      component: Bookmark
    },
    {
      path: '/business-claim',
      name: 'BusinessClaim',
      component: BusinessClaim
    },
    {
      path: '/business/:id',
      name: 'BusinessDetail',
      component: BusinessDetail
    },
    {
      path: '/business-listing',
      name: 'BusinessListing',
      component: BusinessListing
    },
    {
      path: '/review',
      name: 'Review',
      component: Review
    },
    {
      path: '/special-offer',
      name: 'SpecialOffer',
      component: SpecialOffer
    },
    {
      path: '/trending-tags',
      name: 'TrendingTag',
      component: TrendingTag
    },
    {
      path: '/login',
      name: 'UserLogin',
      component: UserLogin
    },
    {
      path: '/register',
      name: 'UserRegistration',
      component: UserRegistration
    },
    // Catch-all route here
    {
      path: '*',
      name: 'NotFound',
      component: NotFoundComponent
    }
  ]
});