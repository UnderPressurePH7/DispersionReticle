package com.dispersionreticle.reduction
{
    import flash.display.Sprite;
    import flash.events.MouseEvent;

    public class ReductionPanel extends Sprite
    {
        private static const BASE_SCALE:Number = 1.1;

        private var _panelNew:ReductionPanelNew;
        private var _panelOld:ReductionPanelOld;
        private var _currentStyle:String = "new";
        private var _isDragging:Boolean = false;
        private var _dragStartX:Number = 0;
        private var _dragStartY:Number = 0;
        private var _onDragEnd:Function = null;
        private var _interfaceScale:Number = 1.0;

        public function ReductionPanel()
        {
            super();

            _panelNew = new ReductionPanelNew();
            _panelOld = new ReductionPanelOld();

            addChild(_panelNew);
            addChild(_panelOld);

            _panelOld.visible = false;

            this.scaleX = BASE_SCALE;
            this.scaleY = BASE_SCALE;

            addEventListener(MouseEvent.MOUSE_DOWN, onMouseDown);
        }

        public function set onDragEndCallback(callback:Function):void
        {
            _onDragEnd = callback;
        }

        public function setStyle(style:String):void
        {
            _currentStyle = style;
            _panelNew.visible = (style == "new");
            _panelOld.visible = (style == "old");
        }

        public function setData(aimingPercent:Number, timeLabel:String, percentLabel:String, aimedLabel:String):void
        {
            if (_currentStyle == "new")
            {
                _panelNew.setData(aimingPercent, timeLabel, percentLabel, aimedLabel);
            }
            else
            {
                _panelOld.setData(aimingPercent, timeLabel, percentLabel, aimedLabel);
            }
        }

        public function setOffset(offsetX:Number, offsetY:Number):void
        {
            this.x = offsetX;
            this.y = offsetY;
        }

        public function setInterfaceScale(scale:Number):void
        {
            if (scale <= 0)
            {
                scale = 1.0;
            }
            _interfaceScale = scale;
            this.scaleX = BASE_SCALE * _interfaceScale;
            this.scaleY = BASE_SCALE * _interfaceScale;
        }

        private function onMouseDown(e:MouseEvent):void
        {
            _isDragging = true;
            _dragStartX = e.stageX - this.x;
            _dragStartY = e.stageY - this.y;

            stage.addEventListener(MouseEvent.MOUSE_MOVE, onMouseMove);
            stage.addEventListener(MouseEvent.MOUSE_UP, onMouseUp);
        }

        private function onMouseMove(e:MouseEvent):void
        {
            if (_isDragging)
            {
                this.x = e.stageX - _dragStartX;
                this.y = e.stageY - _dragStartY;
            }
        }

        private function onMouseUp(e:MouseEvent):void
        {
            _isDragging = false;

            stage.removeEventListener(MouseEvent.MOUSE_MOVE, onMouseMove);
            stage.removeEventListener(MouseEvent.MOUSE_UP, onMouseUp);

            if (_onDragEnd != null)
            {
                _onDragEnd(this.x, this.y);
            }
        }

        public function dispose():void
        {
            removeEventListener(MouseEvent.MOUSE_DOWN, onMouseDown);
            if (stage != null)
            {
                stage.removeEventListener(MouseEvent.MOUSE_MOVE, onMouseMove);
                stage.removeEventListener(MouseEvent.MOUSE_UP, onMouseUp);
            }
        }
    }
}
