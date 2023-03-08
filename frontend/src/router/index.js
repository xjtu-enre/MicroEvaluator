import {createRouter, createWebHistory} from "vue-router";
import Dashboard from "../views/Dashboard.vue";
import Version from "../views/MetricsViews/Version.vue";
import MetricData from "../views/MetricsViews/MetricData.vue";
import Structure from "../views/StructureViews/Structure.vue";
import PackageSize from "../views/StructureViews/PackageSize.vue";
import ControlView from "../views/ControlFlowViews/CView.vue";
import SoftwareHierarchy from "../views/StructureViews/SoftwareHierarchy.vue";
import ModuleCoupling from "../views/StructureViews/ModuleCoupling.vue";
import Catelogue from "../views/StructureViews/hierarchy/Catelogue.vue";
import Cluster from "../views/StructureViews/hierarchy/Cluster.vue";
import HotMap from "../views/MetricsViews/HotMap.vue";
// import Arc from "../views/StructureViews/section/Arc.vue";
import Chord from "../views/StructureViews/section/Chord.vue";
import Section from "../views/StructureViews/section/Section.vue";
import SunBurst from "../views/StructureViews/section/SunBurst.vue";
import Notifications from "../views/Notifications.vue";
import Profile from "../views/Profile.vue";
import SignIn from "../views/SignIn.vue";
import SignUp from "../views/SignUp.vue";

const routes = [
    {
        path: "/",
        name: "/",
        redirect: "/dashboard"
    },
    {
        path: "/dashboard",
        name: "Dashboard",
        component: Dashboard,
    },
    {
        path: "/ControlView",
        name: "ControlView",
        component: ControlView,
    },
    {
        path: "/version",
        name: "Version",
        component: Version,
    },
    {
        path: "/metric",
        name: "MetricData",
        component: MetricData,
    },
    {
        path: "/hotmap",
        name: "HotMap",
        component: HotMap,
    },
    {
        path: "/structure",
        name: "Structure",
        component: Structure,
        children: [
            {
                path: "packagesize",
                name: "PackageSize",
                component: PackageSize,
            },
            {
                path: "softwarehierarchy",
                name: "SoftwareHierarchy",
                component: SoftwareHierarchy,
                children: [
                    {
                        path: "catelogue",
                        name: "Catelogue",
                        component: Catelogue,
                    }, {
                        path: "cluster",
                        name: "Cluster",
                        component: Cluster,
                    }
                ]
            },
            {
                path: "modulecoupling",
                name: "ModuleCoupling",
                component: ModuleCoupling,
                children: [
                    {
                        path: "chord",
                        name: "Chord",
                        component: Chord,
                    },
                    {
                        path: "section",
                        name: "Section",
                        component: Section,
                    },
                    // {
                    //     path: "arc",
                    //     name: "Arc",
                    //     component: Arc,
                    // },
                    {
                        path: "sunburst",
                        name: "SunBurst",
                        component: SunBurst,
                    }
                ]
            },
        ]
    },
    {
        path: "/notifications",
        name: "Notifications",
        component: Notifications,
    },
    {
        path: "/profile",
        name: "Profile",
        component: Profile,
    },
    {
        path: "/sign-in",
        name: "SignIn",
        component: SignIn,
    },
    {
        path: "/sign-up",
        name: "SignUp",
        component: SignUp,
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
    linkActiveClass: "active",
});

export default router;
