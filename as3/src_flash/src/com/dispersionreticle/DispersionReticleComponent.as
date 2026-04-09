package com.dispersionreticle
{
    import flash.events.Event;
    import flash.geom.Point;

    import com.dispersionreticle.config.Config;
    import com.dispersionreticle.reduction.ReductionPanel;

    public class DispersionReticleComponent extends DispersionReticleDisplayable
    {
        private var _config:Config;
        private var _reductionPanel:ReductionPanel;
        private var _dragEndCallback:Function = null;
        private var _reductionEnabled:Boolean = true;
        private var _reductionRuntimeVisible:Boolean = true;

        public function DispersionReticleComponent()
        {
            super();
            _config = new Config();
            _reductionPanel = new ReductionPanel();

            addChild(_reductionPanel);

            _reductionPanel.x = 10;
            _reductionPanel.y = 10;
            _reductionPanel.onDragEndCallback = _onPanelDragEnd;
        }

        public function set onDragEndCallback(callback:Function):void
        {
            _dragEndCallback = callback;
        }

        private function _onPanelDragEnd(offsetX:Number, offsetY:Number):void
        {
            if (_dragEndCallback != null)
            {
                _dragEndCallback(offsetX, offsetY);
            }
        }

        public function as_setReductionData(aimingPercent:Number, timeLabel:String, percentLabel:String, aimedLabel:String):void
        {
            _reductionPanel.setData(aimingPercent, timeLabel, percentLabel, aimedLabel);
        }

        public function as_setReductionConfig(enabled:Boolean, style:String):void
        {
            _config.updateReductionConfig(enabled, style);
            _reductionEnabled = enabled;
            _reductionPanel.visible = _reductionEnabled && _reductionRuntimeVisible;
            _reductionPanel.setStyle(style);
        }

        public function as_setReductionVisible(visible:Boolean):void
        {
            _reductionRuntimeVisible = visible;
            _reductionPanel.visible = _reductionEnabled && _reductionRuntimeVisible;
        }

        public function as_setReductionOffset(offsetX:Number, offsetY:Number):void
        {
            _reductionPanel.setOffset(offsetX, offsetY);
        }

        public function as_setInterfaceScale(scale:Number):void
        {
            _reductionPanel.setInterfaceScale(scale);
        }

        override protected function onDispose():void
        {
            _reductionPanel.dispose();
            super.onDispose();
        }
    }
}
