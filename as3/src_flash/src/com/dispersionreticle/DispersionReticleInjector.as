package com.dispersionreticle
{
    import net.wg.data.constants.generated.*;
    import net.wg.gui.battle.views.*;
    import net.wg.gui.components.containers.*;
    import net.wg.infrastructure.base.AbstractView;
    import net.wg.infrastructure.interfaces.ISimpleManagedContainer;

    public class DispersionReticleInjector extends AbstractView
    {
        public var py_onDragEnd:Function = null;

        private var _component:DispersionReticleComponent = null;

        public function DispersionReticleInjector()
        {
            super();
        }

        override protected function onPopulate():void
        {
            var mainViewContainer:MainViewContainer;
            var windowContainer:ISimpleManagedContainer;
            var idx:int;
            var view:BaseBattlePage = null;

            super.onPopulate();

            mainViewContainer = MainViewContainer(App.containerMgr.getContainer(LAYER_NAMES.LAYER_ORDER.indexOf(LAYER_NAMES.VIEWS)));
            windowContainer = App.containerMgr.getContainer(LAYER_NAMES.LAYER_ORDER.indexOf(LAYER_NAMES.WINDOWS));

            idx = 0;
            while (idx < mainViewContainer.numChildren)
            {
                view = mainViewContainer.getChildAt(idx) as BaseBattlePage;
                if (view)
                {
                    _component = new DispersionReticleComponent();
                    _component.componentName = "DispersionReticleComponent";
                    _component.battlePage = view;
                    _component.onDragEndCallback = _onDragEnd;
                    _component.initBattle();
                    break;
                }
                idx++;
            }

            mainViewContainer.setFocusedView(mainViewContainer.getTopmostView());

            if (windowContainer != null)
            {
                windowContainer.removeChild(this);
            }
        }

        override protected function onDispose():void
        {
            _component = null;
            py_onDragEnd = null;
            super.onDispose();
        }

        private function _onDragEnd(offsetX:Number, offsetY:Number):void
        {
            if (py_onDragEnd != null)
            {
                py_onDragEnd(offsetX, offsetY);
            }
        }
    }
}
