<template>
  <div id="body">
    <div class="card card-body">
      <div id="chart" style="height: 2000px;width: 1000px"></div>
    </div>
  </div>
</template>

<script>
import dagreD3 from "dagre-d3";
import * as d3 from "d3";

export default {
  data() {
    return {
      list: {
        nodes: [
          {id: 0, label: "HomeActivity", shape: "rect", "type": "class"},
          {id: 1, label: "gotoLogin", shape: "rect", "type": "method"},
          {id: 2, label: "boolean b(193)", shape: "rect", "type": "seq"},
          {
            id: 3,
            label: 'final SharedPreferences sharedPreferences = this.getSharedPreferences(\'LOGIN_INFO\', 0)(194)',
            shape: "rect",
            "type": "seq"
          },
          {
            id: 4,
            label: "final SharedPreferences sharedPreferences2 = this.getSharedPreferences(\"USER_INFO\", 0)(195)",
            shape: "rect",
            "type": "seq"
          },
          {
            id: 5,
            label: "if this.app.loginInfo == null || sharedPreferences.getString(\"user_id\", \"\").equals(\"\")(196)",
            shape: "diamond",
            "type": "cond"
          },
          {
            id: 6,
            label: "final Intent intent = new Intent((Context)this, (Class)LoginWebActivity.class)(197)",
            shape: "rect",
            "type": "seq"
          },
          {id: 7, label: "intent.putExtra(\"category\", \"login\")", shape: "rect", "type": "callsite"},
          {id: 8, label: "if b", shape: "diamond", "type": "cond"},
          {id: 9, label: "this.startActivityForResult(intent, 1001)", shape: "rect", "type": "callsite"},
          {id: 10, label: "return", shape: "rect", "type": "seq"},
          {id: 11, label: "this.startActivity(intent)", shape: "rect", "type": "seq"},
          {id: 12, label: "exit", shape: "rect", "type": "seq"}
        ],
        edges: [
          {source: 0, target: 1, label: "Define"},
          {source: 1, target: 2, label: ""},
          {source: 2, target: 3, label: ""},
          {source: 3, target: 4, label: ""},
          {source: 4, target: 5, label: ""},
          {source: 5, target: 6, label: "满足"},
          {source: 5, target: 12, label: "不满足"},
          {source: 6, target: 7, label: ""},
          {source: 7, target: 8, label: ""},
          {source: 8, target: 9, label: "满足"},
          {source: 9, target: 10, label: ""},
          {source: 8, target: 11, label: "不满足"},
          {source: 11, target: 12, label: ""},
          {source: 10, target: 12, label: ""},
        ]
      }
    };
  },
  mounted() {
    //获取D3
    let g = new dagreD3.graphlib.Graph();
    //设置图
    g.setGraph({
      rankdir: 'TB',
    });
    // 添加节点
    this.list.nodes.forEach(item => {
      g.setNode(item.id, {
        //节点标签
        label: this.getLabel(item.label),
        //节点形状
        shape: item.shape,
        //节点样式
        style: this.getColor(item.type),
      })
    });
    // 链接关系
    this.list.edges.forEach(item => {
      g.setEdge(item.source, item.target, {
        //边标签
        label: item.label,
        //边样式
        style: "fill:#fff;stroke:#333;stroke-width:1.5px"
      })
    });
    // 创建渲染器
    let render = new dagreD3.render();
    // 选择 svg 并添加一个g元素作为绘图容器.
    let svgGroup = d3.select('#chart').append('svg').attr('width', 1000)
        .attr('height', 2000).append('g');
    // 在绘图容器上运行渲染器生成流程图.
    render(svgGroup, g);

    //创建提示框
    function createTooltip() {
      return d3.select('#body')
          .append('div')
          .classed('tooltip', true)
          .style('opacity', 0)
          .style('display', 'none');
    };
    let tooltip = createTooltip();
    //tooltip显示
    function tipVisible(textContent) {
      tooltip.transition()
          .duration(400)
          .style('opacity', 0.9)
          .style('display', 'block');
      tooltip.html(textContent)
          .style('left', (d3.event.pageX + 15) + 'px')
          .style('top', (d3.event.pageY + 15) + 'px');
    }
    //tooltip隐藏
    function tipHidden() {
      tooltip.transition()
          .duration(400)
          .style('opacity', 0)
          .style('display', 'none');
    }

    //鼠标悬停显示隐藏tooltip
    svgGroup.selectAll("g.node")
        .on("mouseover", function (v) {
          tipVisible(g.node(v).label);
        })
        .on("mouseout", function (v) {
          console.log(v)
          tipHidden();
        })

  },
  methods: {
    getColor(type) {
      if (type == 'class') {
        return 'fill:#3CB371;stroke:#000'
      } else if (type == 'method') {
        return 'fill:#E6E6FA;stroke:#000'
      } else if (type == 'callsite') {
        return 'fill:#FFD700;stroke:#000'
      }
      return 'fill:#fff;stroke:#000'
    },
    getLabel(label){
      if (label.length > 50) {
        return label.substring(0, 50);
      }
      return label;
    }
  }
};
</script>

<style scoped>
.tooltip {
  position: absolute;
  font-size: 12px;
  text-align: center;
  background-color: white;
  border-radius: 3px;
  box-shadow: rgb(174, 174, 174) 0px 0px 10px;
  cursor: pointer;
  display: inline-block;
  padding: 10px;
}

.tooltip>div {
  padding: 10px;
}
</style>